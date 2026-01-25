"""
File Manager Module for Rex AI Assistant
Handles file operations like opening, searching, organizing files.
Platform: macOS (uses AppleScript/osascript and shell commands)
"""

import subprocess
import os
import shutil
import glob as glob_module
from datetime import datetime, timedelta
from pathlib import Path


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


def run_shell(command):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        print(f"[ERROR] Shell command error: {e}")
        return None


# ========================
# Common Directories
# ========================

HOME = str(Path.home())
DESKTOP = os.path.join(HOME, "Desktop")
DOWNLOADS = os.path.join(HOME, "Downloads")
DOCUMENTS = os.path.join(HOME, "Documents")
PICTURES = os.path.join(HOME, "Pictures")
MUSIC = os.path.join(HOME, "Music")
VIDEOS = os.path.join(HOME, "Movies")

COMMON_DIRS = {
    "desktop": DESKTOP,
    "downloads": DOWNLOADS,
    "documents": DOCUMENTS,
    "pictures": PICTURES,
    "photos": PICTURES,
    "music": MUSIC,
    "videos": VIDEOS,
    "movies": VIDEOS,
    "home": HOME,
}


def resolve_path(path):
    """Resolve a path, expanding ~ and handling common directory names."""
    path = path.strip().strip('"').strip("'")

    # Check if it's a common directory name
    if path.lower() in COMMON_DIRS:
        return COMMON_DIRS[path.lower()]

    # Expand ~ to home directory
    if path.startswith("~"):
        path = os.path.expanduser(path)

    # If it's just a filename, search in common locations
    if not os.path.exists(path) and not os.path.isabs(path):
        # Try common directories
        for dir_path in [DESKTOP, DOWNLOADS, DOCUMENTS, HOME]:
            full_path = os.path.join(dir_path, path)
            if os.path.exists(full_path):
                return full_path

    return path


# ========================
# File Opening
# ========================

def open_file(filepath):
    """Open a file with its default application."""
    filepath = resolve_path(filepath)

    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return f"File not found: {filepath}"

    subprocess.run(["open", filepath])
    print(f"Opened: {filepath}")
    return f"Opened: {os.path.basename(filepath)}"


def open_folder(folderpath):
    """Open a folder in Finder."""
    folderpath = resolve_path(folderpath)

    if not os.path.exists(folderpath):
        print(f"[ERROR] Folder not found: {folderpath}")
        return f"Folder not found: {folderpath}"

    subprocess.run(["open", folderpath])
    print(f"Opened folder: {folderpath}")
    return f"Opened folder: {os.path.basename(folderpath)}"


def open_with_app(filepath, app_name):
    """Open a file with a specific application."""
    filepath = resolve_path(filepath)
    app_name = app_name.strip().strip('"').strip("'")

    if not os.path.exists(filepath):
        return f"File not found: {filepath}"

    subprocess.run(["open", "-a", app_name, filepath])
    return f"Opened {os.path.basename(filepath)} with {app_name}"


def reveal_in_finder(filepath):
    """Reveal a file in Finder."""
    filepath = resolve_path(filepath)

    if not os.path.exists(filepath):
        return f"File not found: {filepath}"

    subprocess.run(["open", "-R", filepath])
    return f"Revealed {os.path.basename(filepath)} in Finder"


# ========================
# File Search
# ========================

def search_files(query, location=None):
    """Search for files matching a query."""
    query = query.strip().strip('"').strip("'")

    if location:
        location = resolve_path(location)
    else:
        location = HOME

    # Use mdfind (Spotlight) for fast search
    cmd = f'mdfind -onlyin "{location}" "{query}"'
    result = run_shell(cmd)

    if result:
        files = result.split("\n")[:10]  # Limit to 10 results
        print(f"Found {len(files)} files matching '{query}':")
        for f in files:
            print(f"  - {f}")
        return files
    else:
        print(f"No files found matching '{query}'")
        return []


def find_by_name(filename, location=None):
    """Find files by exact or partial name."""
    filename = filename.strip().strip('"').strip("'")

    if location:
        location = resolve_path(location)
    else:
        location = HOME

    # Use find command
    cmd = f'find "{location}" -iname "*{filename}*" -maxdepth 5 2>/dev/null | head -20'
    result = run_shell(cmd)

    if result:
        files = [f for f in result.split("\n") if f]
        print(f"Found {len(files)} files:")
        for f in files:
            print(f"  - {f}")
        return files
    return []


def find_by_extension(extension, location=None):
    """Find files by extension."""
    extension = extension.strip().strip('"').strip("'").lstrip(".")

    if location:
        location = resolve_path(location)
    else:
        location = DOWNLOADS

    pattern = os.path.join(location, f"**/*.{extension}")
    files = glob_module.glob(pattern, recursive=True)[:20]

    print(f"Found {len(files)} .{extension} files:")
    for f in files:
        print(f"  - {f}")
    return files


def find_recent_files(hours=24, location=None):
    """Find files modified in the last N hours."""
    try:
        hours = int(str(hours).strip().strip('"').strip("'"))
    except ValueError:
        hours = 24

    if location:
        location = resolve_path(location)
    else:
        location = HOME

    # Use find with mtime
    cmd = f'find "{location}" -type f -mmin -{hours*60} -maxdepth 3 2>/dev/null | head -20'
    result = run_shell(cmd)

    if result:
        files = [f for f in result.split("\n") if f]
        print(f"Found {len(files)} files modified in the last {hours} hours:")
        for f in files:
            print(f"  - {f}")
        return files
    return []


def find_large_files(min_size_mb=100, location=None):
    """Find files larger than specified size in MB."""
    try:
        min_size_mb = int(str(min_size_mb).strip().strip('"').strip("'"))
    except ValueError:
        min_size_mb = 100

    if location:
        location = resolve_path(location)
    else:
        location = HOME

    cmd = f'find "{location}" -type f -size +{min_size_mb}M -maxdepth 4 2>/dev/null | head -20'
    result = run_shell(cmd)

    if result:
        files = [f for f in result.split("\n") if f]
        print(f"Found {len(files)} files larger than {min_size_mb}MB:")
        for f in files:
            size = os.path.getsize(f) / (1024 * 1024)
            print(f"  - {f} ({size:.1f}MB)")
        return files
    return []


# ========================
# File Operations
# ========================

def create_folder(foldername, location=None):
    """Create a new folder."""
    foldername = foldername.strip().strip('"').strip("'")

    if location:
        location = resolve_path(location)
    else:
        location = DESKTOP

    full_path = os.path.join(location, foldername)

    try:
        os.makedirs(full_path, exist_ok=True)
        print(f"Created folder: {full_path}")
        return f"Created folder: {foldername}"
    except Exception as e:
        print(f"[ERROR] Failed to create folder: {e}")
        return f"Failed to create folder: {e}"


def move_file(source, destination):
    """Move a file to a new location."""
    source = resolve_path(source)
    destination = resolve_path(destination)

    if not os.path.exists(source):
        return f"Source not found: {source}"

    try:
        shutil.move(source, destination)
        print(f"Moved {source} to {destination}")
        return f"Moved {os.path.basename(source)} to {destination}"
    except Exception as e:
        return f"Failed to move file: {e}"


def copy_file(source, destination):
    """Copy a file to a new location."""
    source = resolve_path(source)
    destination = resolve_path(destination)

    if not os.path.exists(source):
        return f"Source not found: {source}"

    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        print(f"Copied {source} to {destination}")
        return f"Copied {os.path.basename(source)}"
    except Exception as e:
        return f"Failed to copy file: {e}"


def rename_file(filepath, new_name):
    """Rename a file."""
    filepath = resolve_path(filepath)
    new_name = new_name.strip().strip('"').strip("'")

    if not os.path.exists(filepath):
        return f"File not found: {filepath}"

    directory = os.path.dirname(filepath)
    new_path = os.path.join(directory, new_name)

    try:
        os.rename(filepath, new_path)
        print(f"Renamed to {new_name}")
        return f"Renamed to {new_name}"
    except Exception as e:
        return f"Failed to rename: {e}"


def delete_file(filepath):
    """Move a file to trash (safe delete)."""
    filepath = resolve_path(filepath)

    if not os.path.exists(filepath):
        return f"File not found: {filepath}"

    # Use Finder to move to trash (safer than direct delete)
    script = f'''
    tell application "Finder"
        delete POSIX file "{filepath}"
    end tell
    '''
    run_osascript(script)
    print(f"Moved to trash: {filepath}")
    return f"Moved to trash: {os.path.basename(filepath)}"


def get_file_info(filepath):
    """Get information about a file."""
    filepath = resolve_path(filepath)

    if not os.path.exists(filepath):
        return f"File not found: {filepath}"

    stat = os.stat(filepath)
    info = {
        "name": os.path.basename(filepath),
        "path": filepath,
        "size": f"{stat.st_size / 1024:.2f} KB",
        "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M"),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "is_directory": os.path.isdir(filepath)
    }

    print("File Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")

    return info


# ========================
# Directory Operations
# ========================

def list_directory(dirpath=None):
    """List contents of a directory."""
    if dirpath:
        dirpath = resolve_path(dirpath)
    else:
        dirpath = DESKTOP

    if not os.path.exists(dirpath):
        return f"Directory not found: {dirpath}"

    try:
        contents = os.listdir(dirpath)
        folders = [f for f in contents if os.path.isdir(os.path.join(dirpath, f))]
        files = [f for f in contents if os.path.isfile(os.path.join(dirpath, f))]

        print(f"\nContents of {dirpath}:")
        print(f"Folders ({len(folders)}):")
        for f in sorted(folders)[:10]:
            print(f"  [D] {f}")
        print(f"Files ({len(files)}):")
        for f in sorted(files)[:10]:
            print(f"  [F] {f}")

        return {"folders": folders, "files": files}
    except Exception as e:
        return f"Error listing directory: {e}"


def get_directory_size(dirpath):
    """Get the total size of a directory."""
    dirpath = resolve_path(dirpath)

    if not os.path.exists(dirpath):
        return f"Directory not found: {dirpath}"

    cmd = f'du -sh "{dirpath}"'
    result = run_shell(cmd)

    if result:
        size = result.split()[0]
        print(f"Size of {dirpath}: {size}")
        return f"Size: {size}"
    return "Could not determine size"


# ========================
# File Organization
# ========================

def organize_downloads():
    """Organize downloads folder by file type."""
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
        "Music": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json"],
        "Installers": [".dmg", ".pkg", ".app", ".exe"],
    }

    moved_count = 0

    for filename in os.listdir(DOWNLOADS):
        filepath = os.path.join(DOWNLOADS, filename)

        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()

            for category, extensions in categories.items():
                if ext in extensions:
                    category_dir = os.path.join(DOWNLOADS, category)
                    os.makedirs(category_dir, exist_ok=True)

                    try:
                        shutil.move(filepath, os.path.join(category_dir, filename))
                        moved_count += 1
                    except Exception as e:
                        print(f"[ERROR] Failed to move {filename}: {e}")
                    break

    print(f"Organized {moved_count} files in Downloads")
    return f"Organized {moved_count} files"


def organize_desktop():
    """Organize desktop by moving files to categorized folders."""
    categories = {
        "Screenshots": ["screenshot", "screen shot", "capture"],
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".doc", ".docx", ".txt"],
    }

    moved_count = 0

    for filename in os.listdir(DESKTOP):
        filepath = os.path.join(DESKTOP, filename)

        if os.path.isfile(filepath):
            filename_lower = filename.lower()

            # Check for screenshots
            if any(kw in filename_lower for kw in categories["Screenshots"]):
                dest_dir = os.path.join(DESKTOP, "Screenshots")
                os.makedirs(dest_dir, exist_ok=True)
                try:
                    shutil.move(filepath, os.path.join(dest_dir, filename))
                    moved_count += 1
                except:
                    pass

    print(f"Organized {moved_count} files on Desktop")
    return f"Organized {moved_count} files"


# ========================
# Quick Access
# ========================

def open_downloads():
    """Open Downloads folder."""
    return open_folder(DOWNLOADS)


def open_desktop():
    """Open Desktop folder."""
    return open_folder(DESKTOP)


def open_documents():
    """Open Documents folder."""
    return open_folder(DOCUMENTS)


def open_home():
    """Open Home folder."""
    return open_folder(HOME)


# ========================
# Command Dispatcher
# ========================

COMMANDS = {
    # Opening
    "open": open_file,
    "open_file": open_file,
    "open_folder": open_folder,
    "open_with": open_with_app,
    "reveal": reveal_in_finder,

    # Searching
    "search": search_files,
    "find": find_by_name,
    "find_extension": find_by_extension,
    "recent": find_recent_files,
    "large_files": find_large_files,

    # Operations
    "create_folder": create_folder,
    "move": move_file,
    "copy": copy_file,
    "rename": rename_file,
    "delete": delete_file,
    "info": get_file_info,

    # Directory
    "list": list_directory,
    "ls": list_directory,
    "size": get_directory_size,

    # Organization
    "organize_downloads": organize_downloads,
    "organize_desktop": organize_desktop,

    # Quick access
    "downloads": open_downloads,
    "desktop": open_desktop,
    "documents": open_documents,
    "home": open_home,
}


def handle_command(action, details=None):
    """Executes the given file command dynamically."""
    print(f"[FILES] Action: {action}, Details: {details}")
    if action in COMMANDS:
        if details:
            result = COMMANDS[action](details)
        else:
            result = COMMANDS[action]()
        return result
    else:
        print(f"[ERROR] Unsupported file action: {action}")
        return f"Unsupported action: {action}"


# ========================
# CLI Testing
# ========================

if __name__ == "__main__":
    print("File Manager Module - Test Mode")
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
