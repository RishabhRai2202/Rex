"""
Medium Module for Rex AI Assistant
Handles Medium.com operations like opening articles, searching, and browsing.
"""

import webbrowser
import urllib.parse
import subprocess

# Try to import requests for API/RSS
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


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


# ========================
# Navigation
# ========================

def open_medium():
    """Open Medium homepage."""
    webbrowser.open("https://medium.com")
    print("Opened Medium")
    return "Opened Medium"


def open_feed():
    """Open your Medium feed (requires login)."""
    webbrowser.open("https://medium.com/")
    print("Opened Medium feed")
    return "Opened Medium feed"


def open_bookmarks():
    """Open your saved/bookmarked articles."""
    webbrowser.open("https://medium.com/me/list/reading-list")
    print("Opened Medium bookmarks")
    return "Opened Medium bookmarks"


def open_notifications():
    """Open Medium notifications."""
    webbrowser.open("https://medium.com/me/notifications")
    print("Opened Medium notifications")
    return "Opened notifications"


def open_stats():
    """Open your Medium stats (for writers)."""
    webbrowser.open("https://medium.com/me/stats")
    print("Opened Medium stats")
    return "Opened stats"


def open_stories():
    """Open your stories/drafts."""
    webbrowser.open("https://medium.com/me/stories/drafts")
    print("Opened your stories")
    return "Opened your stories"


def new_story():
    """Create a new story on Medium."""
    webbrowser.open("https://medium.com/new-story")
    print("Opened new story editor")
    return "Opened new story editor"


# ========================
# Search & Discovery
# ========================

def search_medium(query):
    """Search for articles on Medium."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://medium.com/search?q={encoded_query}"
    webbrowser.open(url)
    print(f"Searching Medium for: {query}")
    return f"Searching Medium for: {query}"


def search_tag(tag):
    """Browse articles by tag."""
    tag = tag.strip().strip('"').strip("'").lower().replace(" ", "-")
    url = f"https://medium.com/tag/{tag}"
    webbrowser.open(url)
    print(f"Browsing tag: {tag}")
    return f"Browsing tag: {tag}"


def trending():
    """Open trending articles."""
    webbrowser.open("https://medium.com/explore-topics")
    print("Opened trending topics")
    return "Opened trending topics"


def explore_topic(topic):
    """Explore a specific topic."""
    topic = topic.strip().strip('"').strip("'").lower().replace(" ", "-")
    url = f"https://medium.com/topic/{topic}"
    webbrowser.open(url)
    print(f"Exploring topic: {topic}")
    return f"Exploring topic: {topic}"


# ========================
# Popular Topics
# ========================

def open_programming():
    """Open programming articles."""
    return search_tag("programming")


def open_technology():
    """Open technology articles."""
    return search_tag("technology")


def open_ai():
    """Open AI/ML articles."""
    return search_tag("artificial-intelligence")


def open_startup():
    """Open startup articles."""
    return search_tag("startup")


def open_productivity():
    """Open productivity articles."""
    return search_tag("productivity")


def open_design():
    """Open design articles."""
    return search_tag("design")


def open_data_science():
    """Open data science articles."""
    return search_tag("data-science")


def open_javascript():
    """Open JavaScript articles."""
    return search_tag("javascript")


def open_python():
    """Open Python articles."""
    return search_tag("python")


def open_career():
    """Open career articles."""
    return search_tag("career")


# ========================
# Publications
# ========================

POPULAR_PUBLICATIONS = {
    "towards-data-science": "https://towardsdatascience.com",
    "tds": "https://towardsdatascience.com",
    "hackernoon": "https://hackernoon.com",
    "better-programming": "https://betterprogramming.pub",
    "the-startup": "https://medium.com/swlh",
    "javascript-in-plain-english": "https://javascript.plainenglish.io",
    "level-up-coding": "https://levelup.gitconnected.com",
    "codeburst": "https://codeburst.io",
    "free-code-camp": "https://www.freecodecamp.org/news",
    "ux-collective": "https://uxdesign.cc",
    "ux": "https://uxdesign.cc",
}


def open_publication(pub_name):
    """Open a Medium publication."""
    pub_name = pub_name.strip().strip('"').strip("'").lower().replace(" ", "-")

    if pub_name in POPULAR_PUBLICATIONS:
        url = POPULAR_PUBLICATIONS[pub_name]
    else:
        url = f"https://medium.com/{pub_name}"

    webbrowser.open(url)
    print(f"Opened publication: {pub_name}")
    return f"Opened publication: {pub_name}"


def list_publications():
    """List popular publications."""
    print("Popular Medium Publications:")
    for name, url in POPULAR_PUBLICATIONS.items():
        print(f"  - {name}: {url}")
    return list(POPULAR_PUBLICATIONS.keys())


# ========================
# User Profiles
# ========================

def open_profile(username):
    """Open a user's Medium profile."""
    username = username.strip().strip('"').strip("'").lstrip("@")
    url = f"https://medium.com/@{username}"
    webbrowser.open(url)
    print(f"Opened profile: @{username}")
    return f"Opened profile: @{username}"


def my_profile():
    """Open your own profile."""
    webbrowser.open("https://medium.com/me")
    print("Opened your profile")
    return "Opened your profile"


def followers():
    """Open your followers list."""
    webbrowser.open("https://medium.com/me/following")
    print("Opened followers")
    return "Opened followers"


# ========================
# Reading
# ========================

def open_article(url_or_query):
    """Open a Medium article by URL or search term."""
    url_or_query = url_or_query.strip().strip('"').strip("'")

    if url_or_query.startswith("http"):
        webbrowser.open(url_or_query)
        return f"Opening article: {url_or_query}"
    else:
        # Treat as search
        return search_medium(url_or_query)


def read_later():
    """Open reading list."""
    return open_bookmarks()


# ========================
# RSS Feeds
# ========================

def get_feed_url(username_or_tag):
    """Get RSS feed URL for a user or tag."""
    username_or_tag = username_or_tag.strip().strip('"').strip("'")

    if username_or_tag.startswith("@"):
        # User feed
        username = username_or_tag.lstrip("@")
        url = f"https://medium.com/feed/@{username}"
    elif username_or_tag.startswith("#"):
        # Tag feed
        tag = username_or_tag.lstrip("#")
        url = f"https://medium.com/feed/tag/{tag}"
    else:
        # Assume it's a username
        url = f"https://medium.com/feed/@{username_or_tag}"

    print(f"RSS Feed URL: {url}")
    return url


# ========================
# Settings
# ========================

def open_settings():
    """Open Medium settings."""
    webbrowser.open("https://medium.com/me/settings")
    print("Opened settings")
    return "Opened settings"


def open_membership():
    """Open Medium membership page."""
    webbrowser.open("https://medium.com/membership")
    print("Opened membership page")
    return "Opened membership page"


# ========================
# Partner Program (Writers)
# ========================

def partner_program():
    """Open partner program info."""
    webbrowser.open("https://medium.com/earn")
    print("Opened partner program")
    return "Opened partner program"


def earnings():
    """Open earnings page."""
    webbrowser.open("https://medium.com/me/partner/dashboard")
    print("Opened earnings dashboard")
    return "Opened earnings dashboard"


# ========================
# Command Dispatcher
# ========================

COMMANDS = {
    # Navigation
    "open": open_medium,
    "open_medium": open_medium,
    "feed": open_feed,
    "bookmarks": open_bookmarks,
    "saved": open_bookmarks,
    "notifications": open_notifications,
    "stats": open_stats,
    "stories": open_stories,
    "drafts": open_stories,
    "new": new_story,
    "write": new_story,

    # Search
    "search": search_medium,
    "tag": search_tag,
    "trending": trending,
    "topic": explore_topic,

    # Topics
    "programming": open_programming,
    "technology": open_technology,
    "tech": open_technology,
    "ai": open_ai,
    "ml": open_ai,
    "startup": open_startup,
    "productivity": open_productivity,
    "design": open_design,
    "data_science": open_data_science,
    "javascript": open_javascript,
    "js": open_javascript,
    "python": open_python,
    "career": open_career,

    # Publications
    "publication": open_publication,
    "pub": open_publication,
    "publications": list_publications,

    # Users
    "profile": open_profile,
    "user": open_profile,
    "my_profile": my_profile,
    "me": my_profile,
    "followers": followers,
    "following": followers,

    # Reading
    "article": open_article,
    "read": open_article,
    "read_later": read_later,

    # RSS
    "rss": get_feed_url,
    "feed_url": get_feed_url,

    # Settings
    "settings": open_settings,
    "membership": open_membership,

    # Writers
    "partner": partner_program,
    "earn": partner_program,
    "earnings": earnings,
}


def handle_command(action, details=None):
    """Executes the given Medium command dynamically."""
    print(f"[MEDIUM] Action: {action}, Details: {details}")
    if action in COMMANDS:
        if details:
            result = COMMANDS[action](details)
        else:
            result = COMMANDS[action]()
        return result
    else:
        # Treat unknown action as search
        query = f"{action} {details}" if details else action
        return search_medium(query)


# ========================
# CLI Testing
# ========================

if __name__ == "__main__":
    print("Medium Module - Test Mode")
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
