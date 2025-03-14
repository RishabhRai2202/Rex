import sys
import importlib
from nlp.command_parser import parse_command, get_best_match, load_modules

# Load available modules dynamically
load_modules()

# List of available modules
AVAILABLE_MODULES = {
    "spotify": "modules.spotify",
    "system": "modules.system_commands",
    "medium": "modules.medium",
    "slack": "modules.slack",
    "files": "modules.file_manager",
    "search": "modules.search",
    "akinator": "modules.akinator"
}

def execute_command(user_input):
    """Processes user input and executes the corresponding module action."""
    command, action, details = parse_command(user_input)
    if not command:
        print("[ERROR] Command not recognized.")
        return

    # Find the best matching module
    module_name = get_best_match(command, AVAILABLE_MODULES.keys())

    if not module_name:
        print(f"[ERROR] No matching module found for '{command}'")
        return

    # Import the matched module dynamically
    module_path = AVAILABLE_MODULES[module_name]
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, "handle_command"):
            module.handle_command(action,details)
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