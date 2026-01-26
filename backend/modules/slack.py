"""
Slack Module for Rex AI Assistant
Handles Slack operations like sending messages, checking status, etc.
Note: Requires Slack API token for full functionality.
"""

import subprocess
import webbrowser
import json
import os

# Try to import requests for API calls
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("[WARNING] requests library not installed. Some Slack features won't work.")

# Slack API configuration
SLACK_TOKEN = None
SLACK_API_BASE = "https://slack.com/api"

# Try to load Slack token from secrets file
try:
    secrets_path = '/Users/rishabh/Downloads/secretRex.txt'
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r') as file:
            content = file.read().strip()
            locals_dict = {}
            exec(content, {}, locals_dict)
            SLACK_TOKEN = locals_dict.get('slack_token')
except Exception as e:
    print(f"[WARNING] Could not load Slack token: {e}")


def run_osascript(script):
    """Execute AppleScript and return the result."""
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        print(f"[ERROR] AppleScript error: {e}")
        return None


def slack_api_call(endpoint, method="GET", data=None):
    """Make a Slack API call."""
    if not HAS_REQUESTS:
        return {"error": "requests library not installed"}

    if not SLACK_TOKEN:
        return {"error": "Slack token not configured"}

    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"{SLACK_API_BASE}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        else:
            response = requests.post(url, headers=headers, json=data)

        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ========================
# App Control
# ========================

def open_slack():
    """Open Slack application."""
    script = 'tell application "Slack" to activate'
    run_osascript(script)
    print("Opened Slack")
    return "Opened Slack"


def close_slack():
    """Close Slack application."""
    script = 'tell application "Slack" to quit'
    run_osascript(script)
    print("Closed Slack")
    return "Closed Slack"


def open_slack_web():
    """Open Slack in web browser."""
    webbrowser.open("https://app.slack.com")
    return "Opened Slack in browser"


# ========================
# Messaging (via API)
# ========================

def send_message(channel, message=None):
    """Send a message to a Slack channel."""
    # Handle case where message might be in the channel parameter
    if message is None and " " in channel:
        parts = channel.split(" ", 1)
        channel = parts[0]
        message = parts[1]

    channel = channel.strip().strip('"').strip("'").lstrip("#")
    if message:
        message = message.strip().strip('"').strip("'")
    else:
        return "No message provided"

    if SLACK_TOKEN and HAS_REQUESTS:
        # Use API
        result = slack_api_call("chat.postMessage", "POST", {
            "channel": channel,
            "text": message
        })

        if result.get("ok"):
            print(f"Message sent to #{channel}")
            return f"Message sent to #{channel}"
        else:
            error = result.get("error", "Unknown error")
            print(f"[ERROR] Failed to send message: {error}")
            return f"Failed to send: {error}"
    else:
        # Fallback: Open Slack and try to use AppleScript
        open_slack()
        print(f"[INFO] Please manually send to #{channel}: {message}")
        return f"Slack opened. Please send to #{channel}: {message}"


def send_dm(user, message=None):
    """Send a direct message to a user."""
    if message is None and " " in user:
        parts = user.split(" ", 1)
        user = parts[0]
        message = parts[1]

    user = user.strip().strip('"').strip("'").lstrip("@")
    if message:
        message = message.strip().strip('"').strip("'")
    else:
        return "No message provided"

    if SLACK_TOKEN and HAS_REQUESTS:
        # First, find the user ID
        users_result = slack_api_call("users.list")
        if users_result.get("ok"):
            members = users_result.get("members", [])
            user_id = None
            for member in members:
                if member.get("name") == user or member.get("real_name", "").lower() == user.lower():
                    user_id = member.get("id")
                    break

            if user_id:
                # Open DM conversation
                conv_result = slack_api_call("conversations.open", "POST", {"users": user_id})
                if conv_result.get("ok"):
                    channel_id = conv_result["channel"]["id"]
                    # Send message
                    result = slack_api_call("chat.postMessage", "POST", {
                        "channel": channel_id,
                        "text": message
                    })
                    if result.get("ok"):
                        return f"DM sent to @{user}"

        return f"Could not send DM to @{user}"
    else:
        open_slack()
        return f"Slack opened. Please DM @{user}: {message}"


# ========================
# Status
# ========================

def set_status(status_text, emoji=None):
    """Set your Slack status."""
    status_text = status_text.strip().strip('"').strip("'")

    if emoji:
        emoji = emoji.strip().strip('"').strip("'")
        if not emoji.startswith(":"):
            emoji = f":{emoji}:"
    else:
        # Auto-detect emoji from common status texts
        status_lower = status_text.lower()
        if "meeting" in status_lower:
            emoji = ":calendar:"
        elif "lunch" in status_lower or "eating" in status_lower:
            emoji = ":hamburger:"
        elif "vacation" in status_lower or "holiday" in status_lower:
            emoji = ":palm_tree:"
        elif "sick" in status_lower:
            emoji = ":face_with_thermometer:"
        elif "focus" in status_lower or "busy" in status_lower:
            emoji = ":headphones:"
        elif "away" in status_lower:
            emoji = ":away:"
        else:
            emoji = ":speech_balloon:"

    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("users.profile.set", "POST", {
            "profile": {
                "status_text": status_text,
                "status_emoji": emoji
            }
        })

        if result.get("ok"):
            print(f"Status set to: {emoji} {status_text}")
            return f"Status set to: {emoji} {status_text}"
        else:
            return f"Failed to set status: {result.get('error')}"
    else:
        return f"Status would be: {emoji} {status_text} (API not configured)"


def clear_status():
    """Clear your Slack status."""
    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("users.profile.set", "POST", {
            "profile": {
                "status_text": "",
                "status_emoji": ""
            }
        })

        if result.get("ok"):
            return "Status cleared"
        else:
            return f"Failed to clear status: {result.get('error')}"
    else:
        return "Status clearing requires API token"


def set_away():
    """Set yourself as away."""
    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("users.setPresence", "POST", {"presence": "away"})
        if result.get("ok"):
            return "Set to away"
    return "Set to away (API not configured)"


def set_active():
    """Set yourself as active."""
    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("users.setPresence", "POST", {"presence": "auto"})
        if result.get("ok"):
            return "Set to active"
    return "Set to active (API not configured)"


# ========================
# Channels
# ========================

def list_channels():
    """List all channels."""
    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("conversations.list", "GET", {"types": "public_channel,private_channel"})

        if result.get("ok"):
            channels = result.get("channels", [])
            channel_names = [f"#{ch['name']}" for ch in channels[:20]]
            print("Channels:", channel_names)
            return channel_names
        else:
            return f"Failed to list channels: {result.get('error')}"
    else:
        return "Channel listing requires API token"


def join_channel(channel_name):
    """Join a channel."""
    channel_name = channel_name.strip().strip('"').strip("'").lstrip("#")

    if SLACK_TOKEN and HAS_REQUESTS:
        # First find the channel ID
        channels_result = slack_api_call("conversations.list", "GET", {"types": "public_channel"})

        if channels_result.get("ok"):
            channels = channels_result.get("channels", [])
            channel_id = None
            for ch in channels:
                if ch.get("name") == channel_name:
                    channel_id = ch.get("id")
                    break

            if channel_id:
                result = slack_api_call("conversations.join", "POST", {"channel": channel_id})
                if result.get("ok"):
                    return f"Joined #{channel_name}"

        return f"Could not join #{channel_name}"
    else:
        return "Channel joining requires API token"


def leave_channel(channel_name):
    """Leave a channel."""
    channel_name = channel_name.strip().strip('"').strip("'").lstrip("#")

    if SLACK_TOKEN and HAS_REQUESTS:
        channels_result = slack_api_call("conversations.list", "GET", {"types": "public_channel,private_channel"})

        if channels_result.get("ok"):
            channels = channels_result.get("channels", [])
            channel_id = None
            for ch in channels:
                if ch.get("name") == channel_name:
                    channel_id = ch.get("id")
                    break

            if channel_id:
                result = slack_api_call("conversations.leave", "POST", {"channel": channel_id})
                if result.get("ok"):
                    return f"Left #{channel_name}"

        return f"Could not leave #{channel_name}"
    else:
        return "Channel leaving requires API token"


# ========================
# Unread Messages
# ========================

def check_unreads():
    """Check for unread messages."""
    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("conversations.list", "GET", {
            "types": "public_channel,private_channel,im,mpim",
            "exclude_archived": True
        })

        if result.get("ok"):
            channels = result.get("channels", [])
            unread_channels = []

            for ch in channels:
                if ch.get("unread_count", 0) > 0:
                    name = ch.get("name", ch.get("id"))
                    count = ch.get("unread_count", 0)
                    unread_channels.append(f"#{name}: {count} unread")

            if unread_channels:
                print("Unread messages:")
                for uc in unread_channels[:10]:
                    print(f"  {uc}")
                return unread_channels
            else:
                return "No unread messages"
        else:
            return f"Failed to check unreads: {result.get('error')}"
    else:
        return "Unread checking requires API token"


# ========================
# Do Not Disturb
# ========================

def enable_dnd(minutes=60):
    """Enable Do Not Disturb for specified minutes."""
    try:
        minutes = int(str(minutes).strip().strip('"').strip("'"))
    except ValueError:
        minutes = 60

    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("dnd.setSnooze", "POST", {"num_minutes": minutes})

        if result.get("ok"):
            return f"DND enabled for {minutes} minutes"
        else:
            return f"Failed to enable DND: {result.get('error')}"
    else:
        return f"DND would be enabled for {minutes} minutes (API not configured)"


def disable_dnd():
    """Disable Do Not Disturb."""
    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("dnd.endSnooze", "POST")

        if result.get("ok"):
            return "DND disabled"
        else:
            return f"Failed to disable DND: {result.get('error')}"
    else:
        return "DND disabling requires API token"


# ========================
# Quick Actions
# ========================

def open_channel(channel_name):
    """Open a specific channel in Slack."""
    channel_name = channel_name.strip().strip('"').strip("'").lstrip("#")

    # Try to open via slack:// URL scheme
    webbrowser.open(f"slack://channel?team=&id=&name={channel_name}")
    return f"Opening #{channel_name}"


def search_slack(query):
    """Search in Slack."""
    query = query.strip().strip('"').strip("'")

    if SLACK_TOKEN and HAS_REQUESTS:
        result = slack_api_call("search.messages", "GET", {"query": query})

        if result.get("ok"):
            messages = result.get("messages", {}).get("matches", [])
            if messages:
                results = []
                for msg in messages[:5]:
                    text = msg.get("text", "")[:100]
                    channel = msg.get("channel", {}).get("name", "unknown")
                    results.append(f"#{channel}: {text}")
                return results
            else:
                return "No results found"
        else:
            return f"Search failed: {result.get('error')}"
    else:
        # Fallback: open Slack search
        open_slack()
        return f"Slack opened. Please search for: {query}"


# ========================
# Command Dispatcher
# ========================

COMMANDS = {
    # App control
    "open": open_slack,
    "open_slack": open_slack,
    "close": close_slack,
    "close_slack": close_slack,
    "web": open_slack_web,

    # Messaging
    "send": send_message,
    "send_message": send_message,
    "dm": send_dm,
    "send_dm": send_dm,

    # Status
    "status": set_status,
    "set_status": set_status,
    "clear_status": clear_status,
    "away": set_away,
    "active": set_active,

    # Channels
    "channels": list_channels,
    "list_channels": list_channels,
    "join": join_channel,
    "leave": leave_channel,
    "open_channel": open_channel,

    # Unreads
    "unreads": check_unreads,
    "check_unreads": check_unreads,

    # DND
    "dnd": enable_dnd,
    "enable_dnd": enable_dnd,
    "disable_dnd": disable_dnd,

    # Search
    "search": search_slack,
}


def handle_command(action, details=None):
    """Executes the given Slack command dynamically."""
    print(f"[SLACK] Action: {action}, Details: {details}")
    if action in COMMANDS:
        if details:
            result = COMMANDS[action](details)
        else:
            result = COMMANDS[action]()
        if result:
            print(result)
        return result
    else:
        print(f"[ERROR] Unsupported Slack action: {action}")
        return f"Unsupported action: {action}"


# ========================
# CLI Testing
# ========================

if __name__ == "__main__":
    print("Slack Module - Test Mode")
    print("=" * 40)
    print("Available commands:", list(COMMANDS.keys()))
    print(f"API configured: {SLACK_TOKEN is not None}")
    print("=" * 40)

    while True:
        user_input = input("\nEnter command (or 'exit'): ").strip()
        if user_input.lower() == "exit":
            break

        parts = user_input.split(" ", 1)
        action = parts[0]
        details = parts[1] if len(parts) > 1 else None

        handle_command(action, details)
