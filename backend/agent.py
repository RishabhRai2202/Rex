import sys
import importlib
import inspect
import re
import json
import time
from rapidfuzz import process, fuzz
from nlp.command_parser import parse_command, get_best_match, load_modules
from openai import OpenAI, api_key
import speech_recognition as sr
import pyttsx3
import threading

# Load available modules dynamically
load_modules()

# Configuration
WAKE_WORD = "hey rex"
WAKE_WORD_THRESHOLD = 70  # Fuzzy match threshold percentage


def get_available_modules():
    """Dynamically lists available modules in the system."""
    return {
        "spotify": "modules.spotify",
        "system": "modules.system_commands",
        "medium": "modules.medium",
        "slack": "modules.slack",
        "files": "modules.file_manager",
        "search": "modules.search",
        "akinator": "modules.akinator"
    }


AVAILABLE_MODULES = get_available_modules()


# Add text-to-speech functionality
def speak(text):
    """Convert text to speech using pyttsx3"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Add speech-to-text functionality
def listen(timeout=5, phrase_time_limit=10, prompt="Listening..."):
    """Convert speech to text and return it"""
    recognizer = sr.Recognizer()

    print(prompt)
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Say something!")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Processing speech...")

            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None


def detect_wake_word():
    """Listen specifically for the wake word"""
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening for wake word...")
            # Reduce sensitivity for wake word detection to avoid false positives
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 100  # Higher threshold for wake word to reduce false activations

            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                try:
                    text = recognizer.recognize_google(audio).lower()
                    print(f"Heard: {text}")

                    # Use fuzzy matching for more flexible wake word detection
                    ratio = fuzz.ratio(text, WAKE_WORD)
                    partial_ratio = fuzz.partial_ratio(text, WAKE_WORD)
                    max_ratio = max(ratio, partial_ratio)

                    if max_ratio >= WAKE_WORD_THRESHOLD:
                        print(f"Wake word detected! (Match: {max_ratio}%)")
                        return True
                    elif WAKE_WORD in text:  # Direct substring match as backup
                        print("Wake word detected! (Direct match)")
                        return True

                except sr.UnknownValueError:
                    # Silent failure for wake word detection
                    pass
                except Exception as e:
                    print(f"Error processing potential wake word: {e}")
            except sr.WaitTimeoutError:
                # This is expected, just continue listening
                pass
            except Exception as e:
                print(f"Error while listening for wake word: {e}")
                time.sleep(1)  # Prevent rapid error loops


def get_module_functions(module_name):
    """Fetches available function signatures from a given module."""
    try:
        module_path = AVAILABLE_MODULES.get(module_name)
        if not module_path:
            return {}
        module = importlib.import_module(module_path)
        functions = {}
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("_"):
                continue  # Ignore private/helper functions
            signature = inspect.signature(func)
            functions[name] = {"signature": str(signature)}
        return functions
    except ImportError:
        print(f"[ERROR] Failed to import module {module_name}")
        return {}


def run_nvidia_llm(user_input, available_commands):
    """
    Runs NVIDIA hosted LLama 3.1 Nemotron Ultra to intelligently determine the necessary commands.
    It ensures only essential actions are executed.
    """
    with open('/Users/rishabh/Downloads/secretRex.txt', 'r') as file:
        content = file.read().strip()
        # Use exec() with a local namespace
        locals_dict = {}
        exec(content, {}, locals_dict)
        local_api_key = locals_dict.get("openAISecretKey")
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=local_api_key
    )
    prompt = f"""
 You are an AI that **translates user input into structured step-by-step commands**.
    **Rules:**
    - Identify the correct **module** and **function** based on available commands.
    - Only return **essential actions**—no redundant or unnecessary steps.
    - If multiple steps are required, **split them into separate actions**.
    - Ensure the right **parameters** are extracted from user input.
    - Ignore filler words like "on", "at", "please", "some", "the".
    **Available Modules and Functions:**  
    {json.dumps(available_commands, indent=2)}
    **Examples:**
    - **User Input:** `"Play Rabataa at max volume"`
      **AI Output:**  
      spotify play_track "Rabataa"
      spotify set_volume max
    - **User Input:** `"Play song at max volume"`
      **AI Output:**  
      spotify play
      spotify set_volume max  
    - **User Input:** `"Open Slack and send 'Hello'"`  
      **AI Output:**  
      system open_app Slack
      slack send_message "Hello"
    - **User Input:** `"Turn off WiFi and close Slack"`  
      **AI Output:**  
      system disable_wifi
      system close_app Slack
    **STRICT OUTPUT RULES:**
    - **NO EXPLANATIONS**, only raw step-by-step commands.
    - **Format:** `<module> <function> [parameters]`
    - **DO NOT return JSON. DO NOT include descriptions.**
    - **Only return the structured commands in order.**
    ---
    **User Input:** "{user_input}"
    **Your Response:**
"""
    print("[DEBUG] Sending prompt to NVIDIA LLM")
    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-ultra-253b-v1",
            messages=[
                {"role": "system", "content": "You analyze user requests and convert them to structured commands."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # Lower temperature for more deterministic outputs
            top_p=0.95,
            max_tokens=1024,
            frequency_penalty=0,
            presence_penalty=0
        )
        message = completion.choices[0].message
        content = message.content

        # Some models (like Nemotron) return content in reasoning_content
        if content is None:
            reasoning = getattr(message, 'reasoning_content', None)
            if reasoning:
                print("[DEBUG] Using reasoning_content from response")
                content = reasoning
            else:
                content = ""

        raw_output = content.strip()
        print("[DEBUG] Raw LLM Output:\n", raw_output)
        commands = [line.strip() for line in raw_output.split("\n") if line.strip()]
        return commands
    except Exception as e:
        print(f"[ERROR] LLM processing failed: {e}")
        return []


def execute_command(user_input, voice_mode=False):
    """Processes user input and executes only the necessary actions."""
    # Get all available commands across all modules
    all_available_commands = {}
    for module_name in AVAILABLE_MODULES.keys():
        module_commands = get_module_functions(module_name)
        if module_commands:
            all_available_commands[module_name] = module_commands
    if not all_available_commands:
        error_msg = "[ERROR] No available commands found in any module"
        print(error_msg)
        if voice_mode:
            speak(error_msg)
        return

    # If in voice mode, provide audio confirmation
    if voice_mode and user_input:
        speak("Processing your request")

    command_list = run_nvidia_llm(user_input, all_available_commands)
    if not command_list:
        error_msg = "Sorry, I couldn't recognize a valid command."
        print(error_msg)
        if voice_mode:
            speak(error_msg)
        return

    results = []
    success = True

    for command in command_list:
        parts = command.split(" ", 2)
        if len(parts) < 2:
            print(f"[ERROR] Invalid command format: {command}")
            success = False
            continue

        module_name, action = parts[:2]
        parameters = parts[2] if len(parts) > 2 else None
        module_path = AVAILABLE_MODULES.get(module_name)

        if not module_path:
            print(f"[ERROR] Module '{module_name}' not found.")
            success = False
            continue

        try:
            module = importlib.import_module(module_path)
            if hasattr(module, action):
                # Call the function directly if it exists
                func = getattr(module, action)
                if parameters:
                    result = func(parameters)
                else:
                    result = func()
                if result:
                    results.append(result)
            elif hasattr(module, "handle_command"):
                # Fall back to handle_command if available
                result = module.handle_command(action, parameters)
                if result:
                    results.append(result)
            else:
                print(f"[ERROR] Module '{module_name}' does not have function '{action}' or handle_command.")
                success = False
        except ImportError as e:
            print(f"[ERROR] Failed to import module {module_name}: {e}")
            success = False
        except Exception as e:
            print(f"[ERROR] Error executing command: {e}")
            success = False

    # Provide voice feedback on completion
    if voice_mode:
        if success:
            response = "Command executed successfully"
            if results:
                # Join the results into a single response
                response = ". ".join(str(r) for r in results if r)
            speak(response)
        else:
            speak("I had trouble executing some commands")


def voice_command_loop():
    """Run a continuous loop to listen for the wake word and process commands"""
    speak("Rex is ready. Say 'Hey Rex' to activate.")

    while True:
        try:
            # Wait for wake word
            if detect_wake_word():
                # Visual and audio confirmation that wake word was heard
                print("\n" + "=" * 50)
                print("   REX ACTIVATED - LISTENING FOR COMMAND   ")
                print("=" * 50 + "\n")

                # Play activation sound or speak acknowledgment
                speak("Yes?")

                # Listen for the actual command
                user_input = listen(timeout=5, phrase_time_limit=10, prompt="Listening for command...")

                if user_input:
                    if user_input.lower() in ["exit", "quit", "stop", "goodbye"]:
                        speak("Rex deactivated. Goodbye!")
                        break

                    # Process the voice command
                    execute_command(user_input, voice_mode=True)
                else:
                    speak("I didn't catch that.")

                print("\nListening for wake word again...")

        except KeyboardInterrupt:
            speak("Rex deactivated.")
            break
        except Exception as e:
            print(f"Error in voice command loop: {e}")
            time.sleep(1)  # Prevent rapid error loops


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--voice" or sys.argv[1] == "-v":
            # Start voice command mode with wake word
            voice_command_loop()
        else:
            # Traditional command line mode
            user_input = " ".join(sys.argv[1:])
            execute_command(user_input)
    else:
        # Default to voice mode
        voice_command_loop()