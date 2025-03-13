import os
import subprocess
from sys import stdout
import re


def run_osascript(script):
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        print(result.stdout.strip())
        if result.returncode == 0:
            return result.stdout.strip()  # Removes any extra newlines
        else:
            return None  # Handle failures gracefully
    except Exception as e:
        print(f"Error running AppleScript: {e}")
        return None

# ========================
# Spotify Playback Controls
# ========================

def play():
    run_osascript('tell application "Spotify" to play')


def pause():
    run_osascript('tell application "Spotify" to pause')


def playpause():
    run_osascript('tell application "Spotify" to playpause')


def stop():
    pause()  # No direct stop command in Spotify AppleScript


def next_track():
    run_osascript('tell application "Spotify" to next track')


def previous_track():
    run_osascript('tell application "Spotify" to previous track')


def play_track(track_uri):
    """Plays a specific track or playlist given its Spotify URI."""
    run_osascript(f'tell application "Spotify" to play track "{track_uri}"')


def quit_spotify():
    run_osascript('tell application "Spotify" to quit')


# ========================
# Playback State & Metadata
# ========================

def get_player_state():
    print("GETTING PLAYER STATE: ")
    return run_osascript('tell application "Spotify" to player state')  # stopped, playing, paused


def get_current_track():
    return run_osascript('tell application "Spotify" to current track')


def get_track_name():
    return run_osascript('tell application "Spotify" to name of current track')


def get_track_artist():
    return run_osascript('tell application "Spotify" to artist of current track')


def get_track_album():
    return run_osascript('tell application "Spotify" to album of current track')


def get_album_artist():
    return run_osascript('tell application "Spotify" to album artist of current track')


def get_track_id():
    return run_osascript('tell application "Spotify" to id of current track')


def get_track_url():
    return run_osascript('tell application "Spotify" to spotify url of current track')


def get_track_number():
    return run_osascript('tell application "Spotify" to track number of current track')


def get_disc_number():
    return run_osascript('tell application "Spotify" to disc number of current track')


def get_track_duration():
    return run_osascript('tell application "Spotify" to duration of current track')  # in seconds


def get_track_popularity():
    return run_osascript('tell application "Spotify" to popularity of current track')  # 0-100


def get_played_count():
    return run_osascript('tell application "Spotify" to played count of current track')


def get_track_starred():
    return run_osascript('tell application "Spotify" to starred of current track')


def get_artwork_url():
    return run_osascript('tell application "Spotify" to artwork url of current track')


def get_album_artwork():
    return run_osascript('tell application "Spotify" to artwork of current track')


# ========================
# Player Position & Volume
# ========================

def get_player_position():
    return run_osascript('tell application "Spotify" to player position')  # in seconds


def set_player_position(seconds):
    run_osascript(f'tell application "Spotify" to set player position to {seconds}')


def get_volume():
    return run_osascript('tell application "Spotify" to sound volume')


def set_volume(command):
    """
    Sets the Spotify volume. Extracts volume from the command if needed.
    """
    match = re.search(r'(\d+)', command)  # Extracts first number found
    if match:
        volume = int(match.group(1))
        if 0 <= volume <= 100:
            run_osascript(f'tell application "Spotify" to set sound volume to {volume}')
            print(f"✅ Volume set to {volume}.")
        else:
            print("[ERROR] Invalid volume level. Please provide a number between 0 and 100.")
    else:
        print("[ERROR] No volume level found. Please provide a valid number.")



# ========================
# Shuffle & Repeat Controls
# ========================

def is_shuffling():
    return run_osascript('tell application "Spotify" to shuffling')


def set_shuffle(state=True):
    run_osascript(f'tell application "Spotify" to set shuffling to {str(state).lower()}')


def is_repeating():
    return run_osascript('tell application "Spotify" to repeating')


def set_repeat(state=True):
    run_osascript(f'tell application "Spotify" to set repeating to {str(state).lower()}')


def is_repeating_enabled():
    return run_osascript('tell application "Spotify" to repeating enabled')


def set_repeating_enabled(state=True):
    run_osascript(f'tell application "Spotify" to set repeating enabled to {str(state).lower()}')


# ========================
# App Info
# ========================

def get_spotify_name():
    return run_osascript('tell application "Spotify" to name')


def get_spotify_version():
    return run_osascript('tell application "Spotify" to version')


# ========================
# Command Dispatcher
# ========================

COMMANDS = {
    "play": play,
    "pause": pause,
    "playpause": playpause,
    "stop": stop,
    "next": next_track,
    "previous": previous_track,
    "play_track": play_track,
    "quit": quit_spotify,
    "player_state": get_player_state,
    "track_info": get_current_track,
    "track_name": get_track_name,
    "track_artist": get_track_artist,
    "track_album": get_track_album,
    "album_artist": get_album_artist,
    "track_id": get_track_id,
    "track_url": get_track_url,
    "track_number": get_track_number,
    "disc_number": get_disc_number,
    "track_duration": get_track_duration,
    "track_popularity": get_track_popularity,
    "played_count": get_played_count,
    "track_starred": get_track_starred,
    "artwork_url": get_artwork_url,
    "album_artwork": get_album_artwork,
    "player_position": get_player_position,
    "set_player_position": set_player_position,
    # "volume": get_volume,
    "set_volume": set_volume,
    "shuffling": is_shuffling,
    "set_shuffle": set_shuffle,
    "repeating": is_repeating,
    "set_repeat": set_repeat,
    "repeating_enabled": is_repeating_enabled,
    "set_repeating_enabled": set_repeating_enabled,
    "spotify_name": get_spotify_name,
    "spotify_version": get_spotify_version
}


def handle_command(action, details=None):
    """Executes the given Spotify command dynamically."""
    print("ACTION IN HANDLE COMMAND",action)
    if action in COMMANDS:
        if details:
            COMMANDS[action](details)  # Call with parameter if needed
        else:
            result = COMMANDS[action]()  # Call function without parameters
            if result:
                print(result) # Call function without parameters
    else:
        print(f"Unsupported action '{action}' for Spotify.")


# ========================
# Example Usage (CLI)
# ========================

if __name__ == "__main__":
    while True:
        user_input = input("Enter Spotify command (or 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            break

        parts = user_input.split(" ", 1)
        action = parts[0]
        details = parts[1] if len(parts) > 1 else None

        result = handle_command(action, details)
        if result:
            print(result)