import importlib
import pkgutil
from rapidfuzz import process

MODULES = {}  # Stores module names and their available commands


def load_modules():
    """
    Dynamically loads all modules from the 'modules' package and retrieves their available commands.
    """
    global MODULES
    MODULES.clear()  # Reset before loading

    package_name = "modules"  # Directory containing all module scripts
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
    Extracts the module and action from user input efficiently.
    """
    words = user_input.lower().split()
    if not words:
        print("[DEBUG] No input provided.")
        return None, None

    print(f"[DEBUG] Parsing command: '{user_input}'")

    # Match module first
    matched_module = get_best_match(user_input, MODULES.keys())

    if matched_module:
        print(f"[DEBUG] Matched module: {matched_module}")

        # Extract possible action from user input (excluding module name)
        remaining_words = " ".join([word for word in words if word not in matched_module.split()])
        print(f"[DEBUG] Remaining words after removing module: '{remaining_words}'")

        # Match action only once
        matched_action = get_best_match(remaining_words, MODULES[matched_module]) if remaining_words else None

        print(f"[DEBUG] Matched action: {matched_action if matched_action else 'None'}")
        return matched_module, matched_action or remaining_words

    print("[WARNING] No matching module found.")
    return None, user_input


if __name__ == "__main__":
    load_modules()  # Load available modules dynamically

    while True:
        user_input = input("\nEnter a command: ")
        module, action = parse_command(user_input)
        if module and action:
            print(f"[RESULT] Matched module: {module}, Action: {action}")
        else:
            print("[RESULT] Command not recognized.")