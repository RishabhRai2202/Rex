import importlib
import pkgutil
from rapidfuzz import process

MODULES = {}  # Stores module names and their available commands

def load_modules():
    """Dynamically loads all modules from the 'modules' package and retrieves their available commands."""
    global MODULES
    MODULES.clear()

    package_name = "modules"
    package = importlib.import_module(package_name)

    print("[DEBUG] Loading modules...")

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        try:
            module = importlib.import_module(f"{package_name}.{module_name}")
            if hasattr(module, "COMMANDS") and isinstance(module.COMMANDS, dict):
                MODULES[module_name] = list(module.COMMANDS.keys())
                print(f"[DEBUG] Loaded module: {module_name}, Commands: {MODULES[module_name]}")
            else:
                print(f"[WARNING] Module '{module_name}' does not define COMMANDS properly.")
        except ImportError as e:
            print(f"[ERROR] Error loading module '{module_name}': {e}")

def get_best_match(word, choices, threshold=70):
    """Find the closest match using fuzzy search."""
    print(f"[DEBUG] Searching best match for '{word}' in {choices}")
    match, score, _ = process.extractOne(word, choices) if choices else (None, 0, None)
    print(f"[DEBUG] Found match: '{match}' with score: {score}")
    return match if score >= threshold else None

def parse_command(user_input):
    """
    Extracts the module, action, and parameters from user input efficiently.
    """
    words = user_input.lower().split()
    if not words:
        print("[DEBUG] No input provided.")
        return None, None, None

    print(f"[DEBUG] Parsing command: '{user_input}'")

    # Match module first
    matched_module = get_best_match(user_input, MODULES.keys())

    if matched_module:
        print(f"[DEBUG] Matched module: {matched_module}")

        # Remove module name from words
        remaining_words = [word for word in words if word not in matched_module.split()]
        remaining_text = " ".join(remaining_words)
        print(f"[DEBUG] Remaining words after removing module: '{remaining_text}'")

        # Match action from remaining words
        matched_action = get_best_match(remaining_text, MODULES[matched_module]) if remaining_words else None

        # Extract parameters (words after action)
        if matched_action:
            action_words = matched_action.split()
            remaining_words = [word for word in remaining_words if word not in action_words]
            parameters = " ".join(remaining_words) if remaining_words else None
        else:
            parameters = remaining_text if remaining_text else None

        print(f"[DEBUG] Matched action: {matched_action if matched_action else 'None'}")
        print(f"[DEBUG] Extracted parameters: {parameters if parameters else 'None'}")

        return matched_module, matched_action, parameters

    print("[WARNING] No matching module found.")
    return None, None, user_input


if __name__ == "__main__":
    load_modules()  # Load available modules dynamically

    while True:
        user_input = input("\nEnter a command: ")
        module, action, parameters = parse_command(user_input)
        if module and action:
            print(f"[RESULT] Matched module: {module}, Action: {action}, Parameters: {parameters if parameters else 'None'}")
        elif module:
            print(f"[RESULT] Module detected: {module}, but no valid action found.")
        else:
            print("[RESULT] Command not recognized.")