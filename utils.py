# utils.py — Utility Functions with IST time
from datetime import datetime, timedelta
import random, webbrowser

try:
    import pytz
    IST = pytz.timezone("Asia/Kolkata")
    def now_ist():
        return datetime.now(IST)
except ImportError:
    def now_ist():
        return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_greeting():
    h = now_ist().hour
    if 5  <= h < 12: return "Good morning"
    elif 12 <= h < 17: return "Good afternoon"
    elif 17 <= h < 21: return "Good evening"
    else:              return "Good night"

def tell_time(speak_fn):
    n = now_ist()
    h = n.hour
    period = "morning" if h < 12 else "afternoon" if h < 17 else "evening" if h < 21 else "night"
    r = f"The current time in India is {n.strftime('%I:%M %p')} IST. It is {period}."
    speak_fn(r); return r

def tell_date(speak_fn):
    n = now_ist()
    r = f"Today is {n.strftime('%A, %B %d, %Y')}."
    speak_fn(r); return r

def greet_user(speak_fn):
    g = get_greeting()
    r = f"{g}! I'm Luffy AI, your personal assistant. How can I help you today?"
    speak_fn(r); return r

def tell_joke(speak_fn):
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the developer go broke? He used up all his cache!",
        "Why do Python developers wear glasses? Because they can't C!",
        "A SQL query walks into a bar and asks two tables: Can I join you?",
        "What's a pirate's favorite programming language? Arrr-duino!",
    ]
    r = random.choice(jokes)
    speak_fn(r); return r

def tell_fact(speak_fn):
    facts = [
        "Honey never spoils — archaeologists found 3000 year old honey that was still good!",
        "Octopuses have three hearts and blue blood.",
        "The first computer bug was an actual moth found in a Harvard computer in 1947.",
        "Python was named after Monty Python, not the snake.",
        "Bananas are technically berries, but strawberries are not.",
    ]
    r = random.choice(facts)
    speak_fn(r); return r

def tell_weather(text, speak_fn):
    city = (text.replace("weather in","")
                .replace("weather of","")
                .replace("weather","").strip())
    if city:
        r = f"Looking up weather in {city}!"
        speak_fn(r)
        webbrowser.open(f"https://www.google.com/search?q=weather+in+{city.replace(' ','+')}")
    else:
        r = "Looking up today's weather!"
        speak_fn(r)
        webbrowser.open("https://www.google.com/search?q=weather+today")
    return r

def system_status(speak_fn):
    n = now_ist()
    r = f"All systems running! It is {n.strftime('%I:%M %p IST')} on {n.strftime('%A, %B %d, %Y')}."
    speak_fn(r); return r