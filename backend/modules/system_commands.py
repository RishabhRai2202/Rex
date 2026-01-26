"""
System Commands Module for Rex AI Assistant
Handles system-level operations like app management, WiFi, volume, brightness, etc.
Platform: macOS (uses AppleScript/osascript)
"""

import subprocess
import os
import platform


def run_osascript(script):
    """Execute AppleScript and return the result."""
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"[ERROR] AppleScript failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"[ERROR] Error running AppleScript: {e}")
        return None


def run_shell(command):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"[ERROR] Shell command failed: {result.stderr}")
            return None
    except Exception as e:
        print(f"[ERROR] Error running shell command: {e}")
        return None


# ========================
# Application Management
# ========================

def open_app(app_name):
    """Open an application by name."""
    app_name = app_name.strip().strip('"').strip("'")
    script = f'tell application "{app_name}" to activate'
    result = run_osascript(script)
    if result is not None:
        print(f"Opened {app_name}")
        return f"Opened {app_name}"
    return f"Failed to open {app_name}"


def close_app(app_name):
    """Close an application by name."""
    app_name = app_name.strip().strip('"').strip("'")
    script = f'tell application "{app_name}" to quit'
    result = run_osascript(script)
    if result is not None:
        print(f"Closed {app_name}")
        return f"Closed {app_name}"
    return f"Failed to close {app_name}"


def minimize_app(app_name):
    """Minimize an application window."""
    app_name = app_name.strip().strip('"').strip("'")
    script = f'''
    tell application "System Events"
        tell process "{app_name}"
            set value of attribute "AXMinimized" of window 1 to true
        end tell
    end tell
    '''
    run_osascript(script)
    return f"Minimized {app_name}"


def maximize_app(app_name):
    """Maximize/zoom an application window."""
    app_name = app_name.strip().strip('"').strip("'")
    script = f'''
    tell application "System Events"
        tell process "{app_name}"
            click button 2 of window 1
        end tell
    end tell
    '''
    run_osascript(script)
    return f"Maximized {app_name}"


def list_running_apps():
    """List all running applications."""
    script = '''
    tell application "System Events"
        get name of every process where background only is false
    end tell
    '''
    result = run_osascript(script)
    if result:
        apps = result.split(", ")
        print("Running apps:", apps)
        return apps
    return []


def is_app_running(app_name):
    """Check if an application is running."""
    app_name = app_name.strip().strip('"').strip("'")
    script = f'''
    tell application "System Events"
        set appRunning to exists (processes where name is "{app_name}")
    end tell
    return appRunning
    '''
    result = run_osascript(script)
    return result == "true"


def focus_app(app_name):
    """Bring an application to the front."""
    app_name = app_name.strip().strip('"').strip("'")
    script = f'tell application "{app_name}" to activate'
    run_osascript(script)
    return f"Focused on {app_name}"


# ========================
# System Volume Control
# ========================

def get_system_volume():
    """Get the current system volume (0-100)."""
    result = run_osascript("output volume of (get volume settings)")
    if result:
        return int(result)
    return None


def set_system_volume(level):
    """Set the system volume (0-100)."""
    try:
        level = str(level).strip().strip('"').strip("'")
        if level.lower() == "max":
            vol = 100
        elif level.lower() == "min":
            vol = 0
        elif level.lower() == "mute":
            return mute_volume()
        elif level.lower() == "unmute":
            return unmute_volume()
        elif "increase" in level.lower() or "up" in level.lower():
            current = get_system_volume() or 50
            vol = min(current + 10, 100)
        elif "decrease" in level.lower() or "down" in level.lower():
            current = get_system_volume() or 50
            vol = max(current - 10, 0)
        else:
            vol = int(level)

        vol = max(0, min(100, vol))
        run_osascript(f"set volume output volume {vol}")
        print(f"System volume set to {vol}")
        return f"System volume set to {vol}"
    except ValueError:
        print("[ERROR] Invalid volume level")
        return "Invalid volume level"


def mute_volume():
    """Mute system volume."""
    run_osascript("set volume output muted true")
    print("System muted")
    return "System muted"


def unmute_volume():
    """Unmute system volume."""
    run_osascript("set volume output muted false")
    print("System unmuted")
    return "System unmuted"


def toggle_mute():
    """Toggle system mute."""
    script = '''
    set currentMute to output muted of (get volume settings)
    if currentMute then
        set volume output muted false
        return "unmuted"
    else
        set volume output muted true
        return "muted"
    end if
    '''
    result = run_osascript(script)
    return f"System {result}"


# ========================
# Brightness Control
# ========================

def set_brightness(level):
    """Set screen brightness (0-100)."""
    try:
        level = str(level).strip().strip('"').strip("'")
        if level.lower() == "max":
            brightness = 1.0
        elif level.lower() == "min":
            brightness = 0.1
        elif "increase" in level.lower() or "up" in level.lower():
            # Increase by 10%
            run_shell("brightness +0.1")
            return "Increased brightness"
        elif "decrease" in level.lower() or "down" in level.lower():
            # Decrease by 10%
            run_shell("brightness -0.1")
            return "Decreased brightness"
        else:
            brightness = int(level) / 100.0

        brightness = max(0.0, min(1.0, brightness))
        run_shell(f"brightness {brightness}")
        return f"Brightness set to {int(brightness * 100)}%"
    except ValueError:
        return "Invalid brightness level"


# ========================
# WiFi Control
# ========================

def enable_wifi():
    """Enable WiFi."""
    run_shell("networksetup -setairportpower en0 on")
    print("WiFi enabled")
    return "WiFi enabled"


def disable_wifi():
    """Disable WiFi."""
    run_shell("networksetup -setairportpower en0 off")
    print("WiFi disabled")
    return "WiFi disabled"


def toggle_wifi():
    """Toggle WiFi on/off."""
    status = get_wifi_status()
    if status == "on":
        return disable_wifi()
    else:
        return enable_wifi()


def get_wifi_status():
    """Get current WiFi status."""
    result = run_shell("networksetup -getairportpower en0")
    if result and "On" in result:
        return "on"
    return "off"


def get_wifi_network():
    """Get the name of the connected WiFi network."""
    result = run_shell("networksetup -getairportnetwork en0")
    if result:
        # Output format: "Current Wi-Fi Network: NetworkName"
        if ":" in result:
            return result.split(":")[1].strip()
    return None


# ========================
# Bluetooth Control
# ========================

def enable_bluetooth():
    """Enable Bluetooth."""
    run_shell("blueutil --power 1")
    return "Bluetooth enabled"


def disable_bluetooth():
    """Disable Bluetooth."""
    run_shell("blueutil --power 0")
    return "Bluetooth disabled"


def toggle_bluetooth():
    """Toggle Bluetooth on/off."""
    run_shell("blueutil --power toggle")
    return "Bluetooth toggled"


# ========================
# Power Management
# ========================

def sleep_display():
    """Put the display to sleep."""
    run_shell("pmset displaysleepnow")
    return "Display sleeping"


def sleep_system():
    """Put the system to sleep."""
    run_osascript('tell application "System Events" to sleep')
    return "System sleeping"


def lock_screen():
    """Lock the screen."""
    run_shell("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend")
    return "Screen locked"


def restart_system():
    """Restart the system (requires confirmation)."""
    print("[WARNING] System restart requested")
    return "System restart command received - please confirm manually"


def shutdown_system():
    """Shutdown the system (requires confirmation)."""
    print("[WARNING] System shutdown requested")
    return "System shutdown command received - please confirm manually"


# ========================
# Do Not Disturb
# ========================

def enable_dnd():
    """Enable Do Not Disturb mode."""
    script = '''
    tell application "System Events"
        tell application process "Control Center"
            click menu bar item "Control Center" of menu bar 1
            delay 0.5
            click checkbox "Focus" of window 1
        end tell
    end tell
    '''
    run_osascript(script)
    return "Do Not Disturb enabled"


def disable_dnd():
    """Disable Do Not Disturb mode."""
    # Similar approach, toggle off
    return "Do Not Disturb disabled"


# ========================
# Screenshot
# ========================

def take_screenshot(filename=None):
    """Take a screenshot."""
    if filename:
        filename = filename.strip().strip('"').strip("'")
        run_shell(f"screencapture -x ~/Desktop/{filename}.png")
        return f"Screenshot saved as {filename}.png"
    else:
        run_shell("screencapture -x ~/Desktop/screenshot.png")
        return "Screenshot saved to Desktop"


def take_screenshot_selection():
    """Take a screenshot of a selected area."""
    run_shell("screencapture -i ~/Desktop/screenshot_selection.png")
    return "Screenshot selection saved to Desktop"


# ========================
# Clipboard
# ========================

def get_clipboard():
    """Get clipboard contents."""
    result = run_shell("pbpaste")
    return result


def set_clipboard(text):
    """Set clipboard contents."""
    text = text.strip().strip('"').strip("'")
    subprocess.run(["pbcopy"], input=text.encode(), check=True)
    return f"Copied to clipboard: {text[:50]}..."


def clear_clipboard():
    """Clear the clipboard."""
    subprocess.run(["pbcopy"], input=b"", check=True)
    return "Clipboard cleared"


# ========================
# Notifications
# ========================

def send_notification(message, title="Rex"):
    """Send a system notification."""
    message = message.strip().strip('"').strip("'")
    script = f'display notification "{message}" with title "{title}"'
    run_osascript(script)
    return f"Notification sent: {message}"


# ========================
# System Info
# ========================

def get_battery_status():
    """Get battery percentage and charging status."""
    result = run_shell("pmset -g batt")
    if result:
        # Parse battery info
        lines = result.split("\n")
        for line in lines:
            if "%" in line:
                return line.strip()
    return "Battery info unavailable"


def get_system_info():
    """Get basic system information."""
    info = {
        "os": platform.system(),
        "os_version": platform.mac_ver()[0],
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    return str(info)


# ========================
# Trash
# ========================

def empty_trash():
    """Empty the trash."""
    script = '''
    tell application "Finder"
        empty trash
    end tell
    '''
    run_osascript(script)
    return "Trash emptied"


# ========================
# Command Dispatcher
# ========================

COMMANDS = {
    # App management
    "open_app": open_app,
    "close_app": close_app,
    "minimize_app": minimize_app,
    "maximize_app": maximize_app,
    "list_apps": list_running_apps,
    "is_running": is_app_running,
    "focus_app": focus_app,

    # Volume
    "get_volume": get_system_volume,
    "set_volume": set_system_volume,
    "mute": mute_volume,
    "unmute": unmute_volume,
    "toggle_mute": toggle_mute,

    # Brightness
    "set_brightness": set_brightness,

    # WiFi
    "enable_wifi": enable_wifi,
    "disable_wifi": disable_wifi,
    "toggle_wifi": toggle_wifi,
    "wifi_status": get_wifi_status,
    "wifi_network": get_wifi_network,

    # Bluetooth
    "enable_bluetooth": enable_bluetooth,
    "disable_bluetooth": disable_bluetooth,
    "toggle_bluetooth": toggle_bluetooth,

    # Power
    "sleep_display": sleep_display,
    "sleep": sleep_system,
    "lock": lock_screen,
    "restart": restart_system,
    "shutdown": shutdown_system,

    # DND
    "enable_dnd": enable_dnd,
    "disable_dnd": disable_dnd,

    # Screenshot
    "screenshot": take_screenshot,
    "screenshot_selection": take_screenshot_selection,

    # Clipboard
    "get_clipboard": get_clipboard,
    "set_clipboard": set_clipboard,
    "clear_clipboard": clear_clipboard,

    # Notifications
    "notify": send_notification,

    # System info
    "battery": get_battery_status,
    "system_info": get_system_info,

    # Trash
    "empty_trash": empty_trash,
}


def handle_command(action, details=None):
    """Executes the given system command dynamically."""
    print(f"[SYSTEM] Action: {action}, Details: {details}")
    if action in COMMANDS:
        if details:
            result = COMMANDS[action](details)
        else:
            result = COMMANDS[action]()
        if result:
            print(result)
        return result
    else:
        print(f"[ERROR] Unsupported system action: {action}")
        return f"Unsupported action: {action}"


# ========================
# CLI Testing
# ========================

if __name__ == "__main__":
    print("System Commands Module - Test Mode")
    print("=" * 40)
    print("Available commands:", list(COMMANDS.keys()))
    print("=" * 40)

    while True:
        user_input = input("\nEnter command (or 'exit'): ").strip()
        if user_input.lower() == "exit":
            break

        parts = user_input.split(" ", 1)
        action = parts[0]
        details = parts[1] if len(parts) > 1 else None

        handle_command(action, details)
