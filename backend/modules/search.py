"""
Search Module for Rex AI Assistant
Handles web searches, local searches, and information lookups.
"""

import subprocess
import webbrowser
import urllib.parse
import json

# Optional: Try to import requests for API calls
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
# Web Search
# ========================

def google_search(query):
    """Open a Google search in the default browser."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    webbrowser.open(url)
    print(f"Searching Google for: {query}")
    return f"Searching Google for: {query}"


def youtube_search(query):
    """Search on YouTube."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open(url)
    print(f"Searching YouTube for: {query}")
    return f"Searching YouTube for: {query}"


def wikipedia_search(query):
    """Search on Wikipedia."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://en.wikipedia.org/wiki/Special:Search?search={encoded_query}"
    webbrowser.open(url)
    print(f"Searching Wikipedia for: {query}")
    return f"Searching Wikipedia for: {query}"


def github_search(query):
    """Search on GitHub."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://github.com/search?q={encoded_query}"
    webbrowser.open(url)
    print(f"Searching GitHub for: {query}")
    return f"Searching GitHub for: {query}"


def stackoverflow_search(query):
    """Search on Stack Overflow."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://stackoverflow.com/search?q={encoded_query}"
    webbrowser.open(url)
    print(f"Searching Stack Overflow for: {query}")
    return f"Searching Stack Overflow for: {query}"


def amazon_search(query):
    """Search on Amazon."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.amazon.com/s?k={encoded_query}"
    webbrowser.open(url)
    print(f"Searching Amazon for: {query}")
    return f"Searching Amazon for: {query}"


def maps_search(query):
    """Search on Google Maps."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/maps/search/{encoded_query}"
    webbrowser.open(url)
    print(f"Searching Maps for: {query}")
    return f"Searching Maps for: {query}"


def images_search(query):
    """Search Google Images."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}&tbm=isch"
    webbrowser.open(url)
    print(f"Searching Images for: {query}")
    return f"Searching Images for: {query}"


def duckduckgo_search(query):
    """Search on DuckDuckGo (privacy-focused)."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://duckduckgo.com/?q={encoded_query}"
    webbrowser.open(url)
    print(f"Searching DuckDuckGo for: {query}")
    return f"Searching DuckDuckGo for: {query}"


def reddit_search(query):
    """Search on Reddit."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.reddit.com/search/?q={encoded_query}"
    webbrowser.open(url)
    print(f"Searching Reddit for: {query}")
    return f"Searching Reddit for: {query}"


def twitter_search(query):
    """Search on Twitter/X."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://twitter.com/search?q={encoded_query}"
    webbrowser.open(url)
    print(f"Searching Twitter for: {query}")
    return f"Searching Twitter for: {query}"


def linkedin_search(query):
    """Search on LinkedIn."""
    query = query.strip().strip('"').strip("'")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.linkedin.com/search/results/all/?keywords={encoded_query}"
    webbrowser.open(url)
    print(f"Searching LinkedIn for: {query}")
    return f"Searching LinkedIn for: {query}"


# ========================
# Direct URL Opening
# ========================

def open_url(url):
    """Open a specific URL in the browser."""
    url = url.strip().strip('"').strip("'")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    print(f"Opening: {url}")
    return f"Opening: {url}"


def open_website(site_name):
    """Open common websites by name."""
    site_name = site_name.strip().strip('"').strip("'").lower()

    sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com",
        "twitter": "https://twitter.com",
        "x": "https://twitter.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
        "reddit": "https://www.reddit.com",
        "netflix": "https://www.netflix.com",
        "spotify": "https://open.spotify.com",
        "amazon": "https://www.amazon.com",
        "wikipedia": "https://www.wikipedia.org",
        "stackoverflow": "https://stackoverflow.com",
        "chatgpt": "https://chat.openai.com",
        "claude": "https://claude.ai",
        "medium": "https://medium.com",
        "notion": "https://www.notion.so",
        "figma": "https://www.figma.com",
        "slack": "https://slack.com",
        "discord": "https://discord.com",
        "twitch": "https://www.twitch.tv",
        "news": "https://news.google.com",
    }

    if site_name in sites:
        webbrowser.open(sites[site_name])
        print(f"Opening {site_name}")
        return f"Opening {site_name}"
    else:
        # Try to construct URL
        url = f"https://www.{site_name}.com"
        webbrowser.open(url)
        print(f"Opening {url}")
        return f"Opening {url}"


# ========================
# Local Spotlight Search
# ========================

def spotlight_search(query):
    """Open Spotlight search with a query."""
    query = query.strip().strip('"').strip("'")
    # Open Spotlight and type the query
    script = f'''
    tell application "System Events"
        keystroke space using command down
        delay 0.3
        keystroke "{query}"
    end tell
    '''
    run_osascript(script)
    print(f"Opened Spotlight with: {query}")
    return f"Spotlight search: {query}"


def finder_search(query):
    """Search in Finder."""
    query = query.strip().strip('"').strip("'")
    script = f'''
    tell application "Finder"
        activate
        open (container of (path to home folder))
    end tell
    tell application "System Events"
        keystroke "f" using command down
        delay 0.2
        keystroke "{query}"
    end tell
    '''
    run_osascript(script)
    print(f"Searching Finder for: {query}")
    return f"Finder search: {query}"


# ========================
# Information Lookup
# ========================

def define_word(word):
    """Look up a word definition using macOS Dictionary."""
    word = word.strip().strip('"').strip("'")
    script = f'''
    tell application "Dictionary"
        activate
    end tell
    tell application "System Events"
        keystroke "f" using command down
        delay 0.2
        keystroke "{word}"
        keystroke return
    end tell
    '''
    run_osascript(script)
    print(f"Looking up definition: {word}")
    return f"Looking up: {word}"


def weather_search(location=None):
    """Search for weather information."""
    if location:
        location = location.strip().strip('"').strip("'")
        query = f"weather in {location}"
    else:
        query = "weather"
    return google_search(query)


def news_search(topic=None):
    """Search for news."""
    if topic:
        topic = topic.strip().strip('"').strip("'")
        url = f"https://news.google.com/search?q={urllib.parse.quote(topic)}"
    else:
        url = "https://news.google.com"
    webbrowser.open(url)
    return f"Opening news" + (f" about {topic}" if topic else "")


def translate(text):
    """Open Google Translate with text."""
    text = text.strip().strip('"').strip("'")
    encoded_text = urllib.parse.quote(text)
    url = f"https://translate.google.com/?sl=auto&tl=en&text={encoded_text}"
    webbrowser.open(url)
    print(f"Translating: {text}")
    return f"Translating: {text}"


def calculator(expression=None):
    """Open calculator or search for calculation."""
    if expression:
        expression = expression.strip().strip('"').strip("'")
        return google_search(expression)
    else:
        subprocess.run(["open", "-a", "Calculator"])
        return "Opened Calculator"


def currency_convert(query):
    """Convert currency using Google."""
    query = query.strip().strip('"').strip("'")
    return google_search(f"{query} currency conversion")


def unit_convert(query):
    """Convert units using Google."""
    query = query.strip().strip('"').strip("'")
    return google_search(f"{query} unit conversion")


# ========================
# Smart Search (Auto-detect)
# ========================

def smart_search(query):
    """Intelligently route search based on query content."""
    query = query.strip().strip('"').strip("'").lower()

    # Detect search type from keywords
    if any(kw in query for kw in ["video", "watch", "tutorial"]):
        return youtube_search(query)
    elif any(kw in query for kw in ["code", "programming", "error", "bug"]):
        return stackoverflow_search(query)
    elif any(kw in query for kw in ["repo", "repository", "github", "open source"]):
        return github_search(query)
    elif any(kw in query for kw in ["buy", "price", "shop", "purchase"]):
        return amazon_search(query)
    elif any(kw in query for kw in ["directions", "location", "near me", "how to get to"]):
        return maps_search(query)
    elif any(kw in query for kw in ["weather", "forecast", "temperature"]):
        return weather_search(query)
    elif any(kw in query for kw in ["news", "headlines"]):
        return news_search(query)
    elif any(kw in query for kw in ["define", "meaning", "definition"]):
        word = query.replace("define", "").replace("meaning of", "").replace("definition of", "").strip()
        return define_word(word)
    elif any(kw in query for kw in ["translate"]):
        text = query.replace("translate", "").strip()
        return translate(text)
    elif any(kw in query for kw in ["wiki", "wikipedia", "who is", "what is"]):
        return wikipedia_search(query)
    else:
        # Default to Google
        return google_search(query)


# ========================
# Command Dispatcher
# ========================

COMMANDS = {
    # Web search
    "google": google_search,
    "search": google_search,
    "youtube": youtube_search,
    "wikipedia": wikipedia_search,
    "wiki": wikipedia_search,
    "github": github_search,
    "stackoverflow": stackoverflow_search,
    "amazon": amazon_search,
    "maps": maps_search,
    "images": images_search,
    "duckduckgo": duckduckgo_search,
    "reddit": reddit_search,
    "twitter": twitter_search,
    "linkedin": linkedin_search,

    # URLs
    "open_url": open_url,
    "url": open_url,
    "website": open_website,
    "open_website": open_website,

    # Local search
    "spotlight": spotlight_search,
    "finder": finder_search,

    # Information
    "define": define_word,
    "weather": weather_search,
    "news": news_search,
    "translate": translate,
    "calculator": calculator,
    "calc": calculator,
    "currency": currency_convert,
    "convert": unit_convert,

    # Smart
    "smart_search": smart_search,
    "ask": smart_search,
}


def handle_command(action, details=None):
    """Executes the given search command dynamically."""
    print(f"[SEARCH] Action: {action}, Details: {details}")
    if action in COMMANDS:
        if details:
            result = COMMANDS[action](details)
        else:
            result = COMMANDS[action]()
        return result
    else:
        # If action not found, treat as a search query
        print(f"[SEARCH] Treating as search query: {action} {details or ''}")
        query = f"{action} {details}" if details else action
        return smart_search(query)


# ========================
# CLI Testing
# ========================

if __name__ == "__main__":
    print("Search Module - Test Mode")
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
