import sys
import importlib
import inspect
import re
import json
from rapidfuzz import process
from nlp.command_parser import parse_command, get_best_match, load_modules
from openai import OpenAI, api_key

# Load available modules dynamically
load_modules()


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
        api_key= local_api_key
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

        raw_output = completion.choices[0].message.content.strip()
        print("[DEBUG] Raw LLM Output:\n", raw_output)
        commands = [line.strip() for line in raw_output.split("\n") if line.strip()]
        return commands
    except Exception as e:
        print(f"[ERROR] LLM processing failed: {e}")
        return []


def execute_command(user_input):
    """Processes user input and executes only the necessary actions."""
    # Get all available commands across all modules
    all_available_commands = {}
    for module_name in AVAILABLE_MODULES.keys():
        module_commands = get_module_functions(module_name)
        if module_commands:
            all_available_commands[module_name] = module_commands

    if not all_available_commands:
        print("[ERROR] No available commands found in any module")
        return

    command_list = run_nvidia_llm(user_input, all_available_commands)

    if not command_list:
        print("[ERROR] No valid commands recognized.")
        return

    for command in command_list:
        parts = command.split(" ", 2)
        if len(parts) < 2:
            print(f"[ERROR] Invalid command format: {command}")
            continue

        module_name, action = parts[:2]
        parameters = parts[2] if len(parts) > 2 else None

        module_path = AVAILABLE_MODULES.get(module_name)
        if not module_path:
            print(f"[ERROR] Module '{module_name}' not found.")
            continue

        try:
            module = importlib.import_module(module_path)
            if hasattr(module, action):
                # Call the function directly if it exists
                func = getattr(module, action)
                if parameters:
                    # Simple parameter parsing - this could be enhanced
                    # to handle quoted strings and different parameter types
                    func(parameters)
                else:
                    func()
            elif hasattr(module, "handle_command"):
                # Fall back to handle_command if available
                module.handle_command(action, parameters)
            else:
                print(f"[ERROR] Module '{module_name}' does not have function '{action}' or handle_command.")
        except ImportError as e:
            print(f"[ERROR] Failed to import module {module_name}: {e}")
        except Exception as e:
            print(f"[ERROR] Error executing command: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        execute_command(user_input)
    else:
        print("Usage: python backend/agent.py 'your command here'")