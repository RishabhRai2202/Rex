#!/usr/bin/env python3
"""
Rex AI Assistant - CLI Test Mode
Test all modules without voice input.

Usage:
    python test_cli.py                    # Interactive mode
    python test_cli.py "open Safari"      # Single command mode
    python test_cli.py --module spotify   # Test specific module
"""

import sys
import os
import importlib
import argparse

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import execute_command, get_module_functions, AVAILABLE_MODULES


def print_banner():
    """Print Rex banner."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ███████╗██╗  ██╗     █████╗ ██╗                    ║
║   ██╔══██╗██╔════╝╚██╗██╔╝    ██╔══██╗██║                    ║
║   ██████╔╝█████╗   ╚███╔╝     ███████║██║                    ║
║   ██╔══██╗██╔══╝   ██╔██╗     ██╔══██║██║                    ║
║   ██║  ██║███████╗██╔╝ ██╗    ██║  ██║██║                    ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝                    ║
║                                                               ║
║               CLI Test Mode - No Voice Required               ║
╚═══════════════════════════════════════════════════════════════╝
""")


def list_all_modules():
    """List all available modules and their commands."""
    print("\n" + "=" * 60)
    print("  AVAILABLE MODULES AND COMMANDS")
    print("=" * 60)

    for module_name, module_path in AVAILABLE_MODULES.items():
        print(f"\n┌─ {module_name.upper()} ({module_path})")
        print("│")

        try:
            module = importlib.import_module(module_path)
            if hasattr(module, 'COMMANDS'):
                commands = list(module.COMMANDS.keys())
                for i, cmd in enumerate(commands):
                    prefix = "└─" if i == len(commands) - 1 else "├─"
                    print(f"│  {prefix} {cmd}")
            else:
                print("│  └─ (no COMMANDS dict found)")
        except ImportError as e:
            print(f"│  └─ [ERROR] Could not import: {e}")

        print()


def test_module(module_name):
    """Interactive testing for a specific module."""
    module_path = AVAILABLE_MODULES.get(module_name)
    if not module_path:
        print(f"[ERROR] Module '{module_name}' not found.")
        print(f"Available modules: {list(AVAILABLE_MODULES.keys())}")
        return

    try:
        module = importlib.import_module(module_path)
        commands = list(module.COMMANDS.keys()) if hasattr(module, 'COMMANDS') else []

        print(f"\n{'=' * 50}")
        print(f"  Testing Module: {module_name.upper()}")
        print(f"{'=' * 50}")
        print(f"Available commands: {', '.join(commands)}")
        print("\nFormat: <command> [parameters]")
        print("Type 'back' to return to main menu, 'exit' to quit.\n")

        while True:
            try:
                user_input = input(f"[{module_name}] > ").strip()
            except EOFError:
                break

            if not user_input:
                continue
            if user_input.lower() == "exit":
                sys.exit(0)
            if user_input.lower() == "back":
                return

            parts = user_input.split(" ", 1)
            action = parts[0]
            details = parts[1] if len(parts) > 1 else None

            if hasattr(module, 'handle_command'):
                result = module.handle_command(action, details)
                if result:
                    print(f"Result: {result}")
            elif action in module.COMMANDS:
                func = module.COMMANDS[action]
                try:
                    if details:
                        result = func(details)
                    else:
                        result = func()
                    if result:
                        print(f"Result: {result}")
                except Exception as e:
                    print(f"[ERROR] {e}")
            else:
                print(f"[ERROR] Unknown command: {action}")

    except ImportError as e:
        print(f"[ERROR] Could not import module: {e}")


def natural_language_mode():
    """Test with natural language commands (uses LLM)."""
    print("\n" + "=" * 50)
    print("  NATURAL LANGUAGE MODE (uses LLM)")
    print("=" * 50)
    print("Enter commands in natural language.")
    print("Examples:")
    print("  - 'Play Despacito at max volume'")
    print("  - 'Open Safari and search for Python tutorials'")
    print("  - 'Turn off WiFi'")
    print("  - 'Search YouTube for cooking recipes'")
    print("\nType 'back' to return, 'exit' to quit.\n")

    while True:
        try:
            user_input = input("[NL] > ").strip()
        except EOFError:
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            sys.exit(0)
        if user_input.lower() == "back":
            return

        print("\nProcessing with LLM...")
        execute_command(user_input, voice_mode=False)
        print()


def direct_command_mode():
    """Test with direct module commands (no LLM)."""
    print("\n" + "=" * 50)
    print("  DIRECT COMMAND MODE (no LLM)")
    print("=" * 50)
    print("Format: <module> <command> [parameters]")
    print("Examples:")
    print("  - 'spotify play'")
    print("  - 'spotify play_track Despacito'")
    print("  - 'system open_app Safari'")
    print("  - 'search google Python tutorials'")
    print("  - 'files list downloads'")
    print("\nType 'back' to return, 'exit' to quit.\n")

    while True:
        try:
            user_input = input("[DIRECT] > ").strip()
        except EOFError:
            break

        if not user_input:
            continue
        if user_input.lower() == "exit":
            sys.exit(0)
        if user_input.lower() == "back":
            return

        parts = user_input.split(" ", 2)
        if len(parts) < 2:
            print("[ERROR] Format: <module> <command> [parameters]")
            continue

        module_name = parts[0]
        action = parts[1]
        parameters = parts[2] if len(parts) > 2 else None

        module_path = AVAILABLE_MODULES.get(module_name)
        if not module_path:
            print(f"[ERROR] Module '{module_name}' not found.")
            print(f"Available: {list(AVAILABLE_MODULES.keys())}")
            continue

        try:
            module = importlib.import_module(module_path)

            if hasattr(module, action):
                func = getattr(module, action)
                if parameters:
                    result = func(parameters)
                else:
                    result = func()
                if result:
                    print(f"Result: {result}")
            elif hasattr(module, 'handle_command'):
                result = module.handle_command(action, parameters)
                if result:
                    print(f"Result: {result}")
            else:
                print(f"[ERROR] Command '{action}' not found in {module_name}")

        except Exception as e:
            print(f"[ERROR] {e}")

        print()


def interactive_menu():
    """Main interactive menu."""
    while True:
        print("\n" + "=" * 50)
        print("  REX CLI TEST - MAIN MENU")
        print("=" * 50)
        print("""
  1. Natural Language Mode (uses LLM to parse commands)
  2. Direct Command Mode (module command params)
  3. Test Specific Module
  4. List All Modules & Commands
  5. Quick Tests
  6. Exit
""")
        try:
            choice = input("Select option (1-6): ").strip()
        except EOFError:
            break

        if choice == "1":
            natural_language_mode()
        elif choice == "2":
            direct_command_mode()
        elif choice == "3":
            print(f"\nAvailable modules: {', '.join(AVAILABLE_MODULES.keys())}")
            module = input("Enter module name: ").strip().lower()
            test_module(module)
        elif choice == "4":
            list_all_modules()
        elif choice == "5":
            quick_tests()
        elif choice == "6":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("[ERROR] Invalid option")


def quick_tests():
    """Run quick tests for each module."""
    print("\n" + "=" * 50)
    print("  QUICK TESTS")
    print("=" * 50)

    tests = [
        ("system", "battery", None, "Get battery status"),
        ("system", "list_apps", None, "List running apps"),
        ("files", "list", "downloads", "List downloads folder"),
        ("search", "website", "google", "Open Google"),
        ("spotify", "player_state", None, "Get Spotify state"),
    ]

    print("\nAvailable quick tests:")
    for i, (module, cmd, param, desc) in enumerate(tests, 1):
        print(f"  {i}. [{module}] {cmd} {param or ''} - {desc}")

    print(f"  {len(tests) + 1}. Run ALL tests")
    print(f"  {len(tests) + 2}. Back to menu")

    try:
        choice = input("\nSelect test (1-{}): ".format(len(tests) + 2)).strip()
    except EOFError:
        return

    if choice == str(len(tests) + 2):
        return

    if choice == str(len(tests) + 1):
        # Run all tests
        for module, cmd, param, desc in tests:
            print(f"\n--- Testing: {desc} ---")
            run_quick_test(module, cmd, param)
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tests):
                module, cmd, param, desc = tests[idx]
                print(f"\n--- Testing: {desc} ---")
                run_quick_test(module, cmd, param)
        except ValueError:
            print("[ERROR] Invalid selection")


def run_quick_test(module_name, command, param):
    """Run a single quick test."""
    module_path = AVAILABLE_MODULES.get(module_name)
    if not module_path:
        print(f"[ERROR] Module not found: {module_name}")
        return

    try:
        module = importlib.import_module(module_path)

        if hasattr(module, 'handle_command'):
            result = module.handle_command(command, param)
        elif hasattr(module, command):
            func = getattr(module, command)
            result = func(param) if param else func()
        else:
            result = f"Command {command} not found"

        print(f"Result: {result}")

    except Exception as e:
        print(f"[ERROR] {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Rex AI CLI Test Mode")
    parser.add_argument("command", nargs="*", help="Natural language command to execute")
    parser.add_argument("--module", "-m", help="Test a specific module")
    parser.add_argument("--list", "-l", action="store_true", help="List all modules")
    parser.add_argument("--direct", "-d", action="store_true",
                        help="Use direct mode (format: module command params)")

    args = parser.parse_args()

    if args.list:
        list_all_modules()
        return

    if args.module:
        test_module(args.module)
        return

    if args.command:
        command_str = " ".join(args.command)
        if args.direct:
            # Direct mode: module command params
            parts = command_str.split(" ", 2)
            if len(parts) >= 2:
                module_name = parts[0]
                action = parts[1]
                params = parts[2] if len(parts) > 2 else None

                module_path = AVAILABLE_MODULES.get(module_name)
                if module_path:
                    try:
                        module = importlib.import_module(module_path)
                        if hasattr(module, 'handle_command'):
                            result = module.handle_command(action, params)
                            if result:
                                print(result)
                    except Exception as e:
                        print(f"[ERROR] {e}")
        else:
            # Natural language mode
            execute_command(command_str, voice_mode=False)
        return

    # Interactive mode
    print_banner()
    interactive_menu()


if __name__ == "__main__":
    main()
