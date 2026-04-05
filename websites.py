# websites.py — Website & App Commands
import webbrowser, os

WEBSITES = {
    "google": "https://www.google.com", "youtube": "https://www.youtube.com",
    "github": "https://www.github.com", "gmail": "https://www.gmail.com",
    "whatsapp": "https://web.whatsapp.com", "instagram": "https://www.instagram.com",
    "twitter": "https://www.twitter.com", "linkedin": "https://www.linkedin.com",
    "netflix": "https://www.netflix.com", "chatgpt": "https://chat.openai.com",
    "stackoverflow": "https://www.stackoverflow.com", "amazon": "https://www.amazon.in",
    "reddit": "https://www.reddit.com", "spotify": "https://www.spotify.com",
}
APPS = {
    "notepad": "notepad", "calculator": "calc", "file explorer": "explorer",
    "task manager": "taskmgr", "paint": "mspaint", "vs code": "code",
}

def open_website(text, speak_fn):
    for k, url in WEBSITES.items():
        if k in text:
            speak_fn(f"Opening {k.capitalize()}!")
            webbrowser.open(url)
            return True, f"Opening {k.capitalize()}!"
    return False, None

def open_app(text, speak_fn):
    for k, cmd in APPS.items():
        if k in text:
            speak_fn(f"Opening {k.capitalize()}!")
            os.system(cmd)
            return True, f"Opening {k.capitalize()}!"
    return False, None

def handle_search(text, speak_fn):
    if "search youtube" in text or "youtube search" in text:
        q = text.replace("search youtube for","").replace("search youtube","").strip()
        if q:
            speak_fn(f"Searching YouTube for {q}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={q.replace(' ','+')}")
            return True, f"Searching YouTube for {q}"
    elif "wikipedia" in text:
        q = text.replace("search wikipedia for","").replace("wikipedia","").strip()
        if q:
            speak_fn(f"Searching Wikipedia for {q}")
            webbrowser.open(f"https://en.wikipedia.org/wiki/Special:Search?search={q.replace(' ','+')}")
            return True, f"Searching Wikipedia for {q}"
    elif "search" in text:
        q = text.replace("search for","").replace("search","").strip()
        if q:
            speak_fn(f"Searching Google for {q}")
            webbrowser.open(f"https://www.google.com/search?q={q.replace(' ','+')}")
            return True, f"Searching Google for {q}"
    return False, None