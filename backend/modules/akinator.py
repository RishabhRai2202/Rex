"""
Akinator Module for Rex AI Assistant
Play the Akinator guessing game - think of a character and Akinator will guess it!
Uses the Akinator web service.
"""

import webbrowser
import subprocess

# Try to import akinator library
try:
    from akinator import Akinator, Answer, Theme
    HAS_AKINATOR = True
except ImportError:
    HAS_AKINATOR = False
    print("[INFO] akinator library not installed. Install with: pip install akinator.py")


# Game state
class AkinatorGame:
    """Manages an Akinator game session."""

    def __init__(self):
        self.aki = None
        self.active = False
        self.question_count = 0
        self.theme = "characters"  # characters, animals, objects

    def start(self, theme="characters"):
        """Start a new game."""
        if not HAS_AKINATOR:
            return self._web_fallback()

        self.theme = theme.lower().strip().strip('"').strip("'")

        theme_map = {
            "characters": Theme.Characters,
            "character": Theme.Characters,
            "people": Theme.Characters,
            "animals": Theme.Animals,
            "animal": Theme.Animals,
            "objects": Theme.Objects,
            "object": Theme.Objects,
            "things": Theme.Objects,
        }

        aki_theme = theme_map.get(self.theme, Theme.Characters)

        try:
            self.aki = Akinator()
            question = self.aki.start_game(theme=aki_theme)
            self.active = True
            self.question_count = 1

            print("\n" + "=" * 50)
            print("  AKINATOR - Think of a character!")
            print("=" * 50)
            print(f"\nQuestion {self.question_count}: {question}")
            print("\nAnswer with: yes, no, probably, probably not, don't know")

            return f"Game started! Question 1: {question}"
        except Exception as e:
            print(f"[ERROR] Failed to start Akinator: {e}")
            return self._web_fallback()

    def answer(self, response):
        """Answer the current question."""
        if not self.active or not self.aki:
            return "No active game. Say 'start' to begin!"

        response = response.lower().strip().strip('"').strip("'")

        # Map responses to Akinator answers
        answer_map = {
            "yes": Answer.Yes,
            "y": Answer.Yes,
            "no": Answer.No,
            "n": Answer.No,
            "probably": Answer.Probably,
            "prob": Answer.Probably,
            "probably not": Answer.ProbablyNot,
            "prob not": Answer.ProbablyNot,
            "don't know": Answer.Idk,
            "dont know": Answer.Idk,
            "idk": Answer.Idk,
            "unknown": Answer.Idk,
            "?": Answer.Idk,
        }

        aki_answer = answer_map.get(response)
        if not aki_answer:
            return f"Invalid answer. Use: yes, no, probably, probably not, don't know"

        try:
            # Check if Akinator wants to guess
            if self.aki.progression >= 80:
                self.aki.win()
                guess = self.aki.first_guess

                print("\n" + "=" * 50)
                print("  AKINATOR'S GUESS!")
                print("=" * 50)
                print(f"\nI think it's: {guess.name}")
                print(f"Description: {guess.description}")

                self.active = False
                return f"My guess is: {guess.name} - {guess.description}. Was I right?"

            # Continue asking
            question = self.aki.answer(aki_answer)
            self.question_count += 1

            print(f"\nQuestion {self.question_count}: {question}")
            print(f"(Progress: {self.aki.progression:.1f}%)")

            return f"Question {self.question_count}: {question}"

        except Exception as e:
            print(f"[ERROR] Error during game: {e}")
            self.active = False
            return f"Game error: {e}"

    def back(self):
        """Go back to previous question."""
        if not self.active or not self.aki:
            return "No active game."

        try:
            question = self.aki.back()
            self.question_count = max(1, self.question_count - 1)
            print(f"\nQuestion {self.question_count}: {question}")
            return f"Going back. Question {self.question_count}: {question}"
        except Exception as e:
            return f"Cannot go back: {e}"

    def quit(self):
        """Quit the current game."""
        self.active = False
        self.aki = None
        self.question_count = 0
        print("Game ended.")
        return "Game ended. Say 'start' to play again!"

    def status(self):
        """Get current game status."""
        if not self.active:
            return "No active game. Say 'start' to begin!"

        return f"Game active. Question #{self.question_count}, Progress: {self.aki.progression:.1f}%"

    def _web_fallback(self):
        """Fall back to web version."""
        webbrowser.open("https://en.akinator.com/")
        print("Opening Akinator in browser...")
        return "Opening Akinator in browser (library not installed)"


# Global game instance
game = AkinatorGame()


# ========================
# Game Commands
# ========================

def start_game(theme="characters"):
    """Start a new Akinator game."""
    return game.start(theme)


def answer_question(response):
    """Answer the current question."""
    return game.answer(response)


def yes():
    """Answer yes."""
    return game.answer("yes")


def no():
    """Answer no."""
    return game.answer("no")


def probably():
    """Answer probably."""
    return game.answer("probably")


def probably_not():
    """Answer probably not."""
    return game.answer("probably not")


def dont_know():
    """Answer don't know."""
    return game.answer("don't know")


def go_back():
    """Go back to previous question."""
    return game.back()


def quit_game():
    """Quit the current game."""
    return game.quit()


def game_status():
    """Get current game status."""
    return game.status()


# ========================
# Web Versions
# ========================

def open_akinator():
    """Open Akinator in browser."""
    webbrowser.open("https://en.akinator.com/")
    print("Opening Akinator in browser")
    return "Opening Akinator in browser"


def open_akinator_characters():
    """Open Akinator characters mode in browser."""
    webbrowser.open("https://en.akinator.com/game")
    return "Opening Akinator (Characters) in browser"


def open_akinator_animals():
    """Open Akinator animals mode in browser."""
    webbrowser.open("https://en.akinator.com/theme-selection")
    return "Opening Akinator (Animals) in browser"


# ========================
# Quick Play Modes
# ========================

def play_characters():
    """Start a game with characters theme."""
    return start_game("characters")


def play_animals():
    """Start a game with animals theme."""
    return start_game("animals")


def play_objects():
    """Start a game with objects theme."""
    return start_game("objects")


# ========================
# Command Dispatcher
# ========================

COMMANDS = {
    # Game control
    "start": start_game,
    "play": start_game,
    "begin": start_game,
    "new": start_game,

    # Answers
    "answer": answer_question,
    "yes": yes,
    "y": yes,
    "no": no,
    "n": no,
    "probably": probably,
    "prob": probably,
    "probably_not": probably_not,
    "dont_know": dont_know,
    "idk": dont_know,

    # Navigation
    "back": go_back,
    "previous": go_back,
    "undo": go_back,

    # Game management
    "quit": quit_game,
    "stop": quit_game,
    "end": quit_game,
    "exit": quit_game,
    "status": game_status,

    # Web
    "open": open_akinator,
    "web": open_akinator,
    "browser": open_akinator,

    # Quick modes
    "characters": play_characters,
    "people": play_characters,
    "animals": play_animals,
    "objects": play_objects,
    "things": play_objects,
}


def handle_command(action, details=None):
    """Executes the given Akinator command dynamically."""
    print(f"[AKINATOR] Action: {action}, Details: {details}")

    # If game is active and action looks like an answer
    if game.active and action.lower() in ["yes", "no", "probably", "probably not", "idk", "y", "n"]:
        return game.answer(action)

    if action in COMMANDS:
        if details:
            result = COMMANDS[action](details)
        else:
            result = COMMANDS[action]()
        return result
    else:
        # If game is active, treat unknown input as answer
        if game.active:
            return game.answer(action)

        print(f"[ERROR] Unsupported Akinator action: {action}")
        return f"Unsupported action: {action}. Try 'start' to begin a game."


# ========================
# Interactive CLI Mode
# ========================

def interactive_game():
    """Run an interactive Akinator game in the terminal."""
    print("\n" + "=" * 50)
    print("  WELCOME TO AKINATOR!")
    print("  Think of a character, and I'll guess it.")
    print("=" * 50)

    if not HAS_AKINATOR:
        print("\n[WARNING] akinator library not installed.")
        print("Install with: pip install akinator.py")
        print("Opening web version instead...")
        open_akinator()
        return

    print("\nChoose a theme:")
    print("1. Characters (people, fictional characters)")
    print("2. Animals")
    print("3. Objects")

    choice = input("\nEnter choice (1-3): ").strip()

    theme_map = {"1": "characters", "2": "animals", "3": "objects"}
    theme = theme_map.get(choice, "characters")

    result = start_game(theme)
    print(result)

    while game.active:
        print("\nOptions: yes(y), no(n), probably(p), probably not(pn), don't know(?), back(b), quit(q)")
        user_input = input("Your answer: ").strip().lower()

        if user_input in ["q", "quit", "exit"]:
            quit_game()
            break
        elif user_input in ["b", "back"]:
            print(go_back())
        elif user_input in ["y", "yes"]:
            result = yes()
            print(result)
        elif user_input in ["n", "no"]:
            result = no()
            print(result)
        elif user_input in ["p", "probably"]:
            result = probably()
            print(result)
        elif user_input in ["pn", "probably not"]:
            result = probably_not()
            print(result)
        elif user_input in ["?", "idk", "don't know", "dont know"]:
            result = dont_know()
            print(result)
        else:
            print("Invalid input. Use: yes, no, probably, probably not, don't know")

    print("\nThanks for playing!")


# ========================
# CLI Testing
# ========================

if __name__ == "__main__":
    print("Akinator Module - Test Mode")
    print("=" * 40)
    print("Available commands:", list(COMMANDS.keys()))
    print(f"Library installed: {HAS_AKINATOR}")
    print("=" * 40)

    mode = input("\nEnter 'play' for interactive game or 'test' for command testing: ").strip().lower()

    if mode == "play":
        interactive_game()
    else:
        while True:
            user_input = input("\nEnter command (or 'exit'): ").strip()
            if user_input.lower() == "exit":
                break

            parts = user_input.split(" ", 1)
            action = parts[0]
            details = parts[1] if len(parts) > 1 else None

            result = handle_command(action, details)
            if result:
                print(result)
