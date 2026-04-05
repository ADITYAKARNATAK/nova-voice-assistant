# ============================================
# websites.py — Website & App Handler
# Luffy AI Assistant — Final Version
# ============================================

import webbrowser
import os

WEBSITES = {
    "google"        : "https://www.google.com",
    "youtube"       : "https://www.youtube.com",
    "github"        : "https://www.github.com",
    "gmail"         : "https://www.gmail.com",
    "whatsapp"      : "https://web.whatsapp.com",
    "instagram"     : "https://www.instagram.com",
    "twitter"       : "https://www.twitter.com",
    "linkedin"      : "https://www.linkedin.com",
    "netflix"       : "https://www.netflix.com",
    "chatgpt"       : "https://chat.openai.com",
    "stackoverflow" : "https://www.stackoverflow.com",
    "amazon"        : "https://www.amazon.in",
    "reddit"        : "https://www.reddit.com",
    "spotify"       : "https://www.spotify.com",
    "maps"          : "https://www.google.com/maps",
    "news"          : "https://news.google.com",
    "claude"        : "https://claude.ai",
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
}


def open_website(text, speak_fn):
    for keyword, url in WEBSITES.items():
        if keyword in text:
            response = f"Shishishi! Opening {keyword.capitalize()} — full speed ahead!"
            speak_fn(response)
            webbrowser.open(url)
            return True, response
    return False, None


def open_app(text, speak_fn):
    for keyword, command in APPS.items():
        if keyword in text:
            response = f"Aye aye! Opening {keyword.capitalize()} right now!"
            speak_fn(response)
            os.system(command)
            return True, response
    return False, None


def handle_search(text, speak_fn):
    if "search youtube" in text or "youtube search" in text:
        query = text.replace("search youtube for", "").replace("search youtube", "").strip()
        if query:
            response = f"Searching YouTube for {query} — Usopp would love this!"
            speak_fn(response)
            webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        else:
            response = "What should I search on YouTube, nakama?"
            speak_fn(response)
        return True, response

    elif "wikipedia" in text:
        query = text.replace("search wikipedia for", "").replace("wikipedia", "").strip()
        if query:
            response = f"Searching Wikipedia for {query} — Robin would be proud!"
            speak_fn(response)
            webbrowser.open(f"https://en.wikipedia.org/wiki/Special:Search?search={query.replace(' ', '+')}")
        else:
            response = "What should I search on Wikipedia?"
            speak_fn(response)
        return True, response

    elif "search for" in text or "search" in text:
        query = text.replace("search for", "").replace("search", "").strip()
        if query:
            response = f"Searching Google for {query}!"
            speak_fn(response)
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        else:
            response = "What should I search for, nakama?"
            speak_fn(response)
        return True, response

    return False, None