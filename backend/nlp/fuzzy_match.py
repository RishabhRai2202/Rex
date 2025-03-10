from difflib import get_close_matches

def fuzzy_match(command, available_commands):
    """
    Uses fuzzy matching to find the closest available command.
    """
    matches = get_close_matches(command, available_commands, n=1, cutoff=0.6)
    return matches[0] if matches else None