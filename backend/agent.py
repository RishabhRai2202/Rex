import sys
import importlib
import subprocess
import inspect
import re
import json
from rapidfuzz import process
from nlp.command_parser import parse_command, get_best_match, load_modules

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
            category = "getter" if len(signature.parameters) == 0 else "action"
            functions[name] = {"signature": str(signature), "category": category}

        return functions

    except ImportError:
        print(f"[ERROR] Failed to import module {module_name}")
        return {}


def run_ollama(user_input, available_commands):
    """
    Runs Ollama to intelligently determine the necessary commands.
    It ensures only essential actions are executed.
    """
    prompt = f"""
    You are an AI assistant that decides which commands are absolutely necessary
    based on the user's request. 

    - Identify the correct module and function based on available commands.
    - Only choose the essential commands, avoiding redundant actions.
    - Prioritize actions that directly satisfy the request.
    - If multiple steps are needed, optimize them into the fewest possible calls.
    - Return only the final necessary commands.

    Available Modules and Commands:
    {json.dumps(available_commands, indent=2)}

    User Input:
    "{user_input}"

    STRICT OUTPUT RULES:
    - DO NOT return explanations, reasoning, or any text other than raw commands.
    - DO NOT repeat the same function unnecessarily.
    - DO NOT output JSON, explanations, or markdown formatting.
    - ONLY return the required commands in the format:

      <module> <function> [optional parameters]

    Example Outputs:

    User: "Play my favorite song on max volume"
    Output:
      spotify play
      spotify set_volume max

    User: "Search Python tutorials and open the first result"
    Output:
      search query "Python tutorials"
      system open_url <top_result>

    User: "Turn off WiFi and close Slack"
    Output:
      system disable_wifi
      system close_app Slack
      
    User: "spotify play Maniac"  
    Output: 
        spotify play_track Maniac
        
    User: "spotify play song at max volume"    
    Output: 
        spotify play 
        spotify set_volume max
        
    You have to make intelligent decision to remove unwanted parts from the command as well. YOu are intelligent enought to do it pls do it.    

    Now process the input and return ONLY the required commands.
    """

    print("[DEBUG] Sending prompt to Ollama:\n", prompt)

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2"],
            input=prompt,
            text=True,
            capture_output=True
        )

        raw_output = result.stdout.strip()
        print("[DEBUG] Raw Ollama Output:\n", raw_output)

        commands = [line.strip() for line in raw_output.split("\n") if line.strip()]
        return commands

    except Exception as e:
        print(f"[ERROR] Ollama processing failed: {e}")
        return []


def execute_command(user_input):
    """Processes user input and executes only the necessary actions."""
    module_name = get_best_match(user_input, AVAILABLE_MODULES.keys())

    if not module_name:
        print(f"[ERROR] No matching module found for '{user_input}'")
        return

    available_commands = get_module_functions(module_name)
    if not available_commands:
        print(f"[ERROR] No commands found in module '{module_name}'")
        return

    command_list = run_ollama(user_input, available_commands)

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
            if hasattr(module, "handle_command"):
                module.handle_command(action, parameters)
            else:
                print(f"[ERROR] Module '{module_name}' does not have a handle_command function.")
        except ImportError as e:
            print(f"[ERROR] Failed to import module {module_name}: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        execute_command(user_input)
    else:
        print("Usage: python backend/agent.py 'your command here'")