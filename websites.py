# ============================================
# websites.py — Website & App Handler
# Nova Voice Assistant — Final Version
# ============================================

import webbrowser
import os


# ============================================
# WEBSITE DICTIONARY
# ============================================

WEBSITES = {
    "google"       : "https://www.google.com",
    "youtube"      : "https://www.youtube.com",
    "github"       : "https://www.github.com",
    "gmail"        : "https://www.gmail.com",
    "whatsapp"     : "https://web.whatsapp.com",
    "instagram"    : "https://www.instagram.com",
    "twitter"      : "https://www.twitter.com",
    "linkedin"     : "https://www.linkedin.com",
    "netflix"      : "https://www.netflix.com",
    "chatgpt"      : "https://chat.openai.com",
    "stackoverflow": "https://www.stackoverflow.com",
    "amazon"       : "https://www.amazon.in",
    "reddit"       : "https://www.reddit.com",
    "spotify"      : "https://www.spotify.com",
    "maps"         : "https://www.google.com/maps",
    "news"         : "https://news.google.com",
    "claude"       : "https://claude.ai",
}

APPS = {
    "notepad"        : "notepad",
    "calculator"     : "calc",
    "file explorer"  : "explorer",
    "task manager"   : "taskmgr",
    "paint"          : "mspaint",
    "cmd"            : "start cmd",
    "command prompt" : "start cmd",
    "vs code"        : "code",
    "word"           : "start winword",
    "excel"          : "start excel",
}


# ============================================
# OPEN WEBSITE
# ============================================

def open_website(text, speak_fn):
    for keyword, url in WEBSITES.items():
        if keyword in text:
            response = f"Opening {keyword.capitalize()} for you!"
            speak_fn(response)
            webbrowser.open(url)
            return True, response
    return False, None


# ============================================
# OPEN APP
# ============================================

def open_app(text, speak_fn):
    for keyword, command in APPS.items():
        if keyword in text:
            response = f"Opening {keyword.capitalize()}!"
            speak_fn(response)
            os.system(command)
            return True, response
    return False, None


# ============================================
# HANDLE SEARCH
# ============================================

def handle_search(text, speak_fn):

    # YouTube search — check before Google
    if "search youtube" in text or "youtube search" in text:
        query = text.replace("search youtube for", "")
        query = query.replace("search youtube", "").strip()
        if query:
            response = f"Searching YouTube for {query}"
            speak_fn(response)
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            )
        else:
            response = "What should I search on YouTube?"
            speak_fn(response)
        return True, response

    # Wikipedia
    elif "wikipedia" in text:
        query = text.replace("search wikipedia for", "")
        query = query.replace("wikipedia", "").strip()
        if query:
            response = f"Searching Wikipedia for {query}"
            speak_fn(response)
            webbrowser.open(
                f"https://en.wikipedia.org/wiki/Special:Search?search={query.replace(' ', '+')}"
            )
        else:
            response = "What should I search on Wikipedia?"
            speak_fn(response)
        return True, response

    # Google search
    elif "search for" in text or "search" in text:
        query = text.replace("search for", "").replace("search", "").strip()
        if query:
            response = f"Searching Google for {query}"
            speak_fn(response)
            webbrowser.open(
                f"https://www.google.com/search?q={query.replace(' ', '+')}"
            )
        else:
            response = "What would you like me to search for?"
            speak_fn(response)
        return True, response

    return False, None