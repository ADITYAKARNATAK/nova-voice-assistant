# ============================================
# utils.py — Smart Utility Functions
# Luffy AI Assistant — Final Version
# ============================================

from datetime import datetime
import webbrowser
import random


def tell_time(speak_fn):
    now = datetime.now()
    hour = now.hour
    formatted_time = now.strftime("%I:%M %p")
    if 5 <= hour < 12:
        period = "in the morning"
    elif 12 <= hour < 17:
        period = "in the afternoon"
    elif 17 <= hour < 21:
        period = "in the evening"
    else:
        period = "at night"
    response = f"It is {formatted_time} {period}."
    if hour == 0 and now.minute < 5:
        response += " It's midnight! Even pirates need sleep!"
    elif hour == 12 and now.minute < 5:
        response += " It's noon! Meat time!"
    elif 4 <= hour < 6:
        response += " You're up early, like a true pirate setting sail!"
    elif hour >= 23:
        response += " It's late! Even the Grand Line sleeps sometimes!"
    speak_fn(response)
    return response


def tell_date(speak_fn):
    now = datetime.now()
    day_name   = now.strftime("%A")
    month_name = now.strftime("%B")
    day_number = now.strftime("%d")
    year       = now.strftime("%Y")
    response = f"Today is {day_name}, {month_name} {day_number}, {year}."
    if day_name == "Monday":
        response += " New week, new adventure! Set sail!"
    elif day_name == "Friday":
        response += " It's Friday! The party's starting on the Thousand Sunny!"
    elif day_name in ["Saturday", "Sunday"]:
        response += " Weekend! Time for a feast like a true pirate!"
    speak_fn(response)
    return response


def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning, nakama"
    elif 12 <= hour < 17:
        return "Good afternoon, nakama"
    elif 17 <= hour < 21:
        return "Good evening, nakama"
    else:
        return "Good night, nakama"


def greet_user(speak_fn):
    greeting = get_greeting()
    response = f"{greeting}! I'm Luffy, your AI first mate! I'm gonna be King of the Pirates AND your best assistant!"
    speak_fn(response)
    return response


def tell_joke(speak_fn):
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs, and I hate bugs unless they're Sea Kings!",
        "Why did the pirate fail programming? Because he kept using the wrong Arrr-ray!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem — ask Franky!",
        "Why do Python programmers wear glasses? Because they can't C! Get it? Like Sea? Haha!",
        "What did Zoro say to the compiler? I'm going to need more than one path to get there!",
        "A SQL query walks into a bar and asks two tables: Can I join you? Just like the Straw Hat crew!",
        "Why was Nami always good at coding? She always knew how to handle exceptions... and money!",
    ]
    joke = random.choice(jokes)
    speak_fn(joke)
    return joke


def tell_weather(text, speak_fn):
    if "weather in" in text:
        city = text.replace("weather in", "").strip()
    elif "weather of" in text:
        city = text.replace("weather of", "").strip()
    elif "weather" in text:
        city = text.replace("weather", "").strip()
    else:
        city = ""
    if city:
        response = f"Aye aye! Checking the weather in {city} for our voyage!"
        speak_fn(response)
        webbrowser.open(f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}")
    else:
        response = "Checking today's weather — Nami would want to know before we set sail!"
        speak_fn(response)
        webbrowser.open("https://www.google.com/search?q=weather+today")
    return response


def tell_fact(speak_fn):
    facts = [
        "Honey never spoils. Archaeologists found 3000 year old honey in Egyptian tombs that was still good!",
        "A group of flamingos is called a flamboyance. Even cooler than a pirate crew name!",
        "Octopuses have three hearts and blue blood. Haki training must be intense for them!",
        "The first computer bug was an actual bug — a moth found in a Harvard computer in 1947!",
        "Python was named after Monty Python, not the snake. Though snakes are cool like Sea Kings!",
        "Bananas are technically berries, but strawberries are not. Chopper finds this medically fascinating!",
        "There are more possible chess games than atoms in the observable universe. Even Zoro would get lost in that!",
        "A day on Venus is longer than a year on Venus. Navigation in space is harder than the Grand Line!",
    ]
    fact = random.choice(facts)
    response = f"Here's an interesting fact, nakama: {fact}"
    speak_fn(response)
    return response


def system_status(speak_fn):
    now = datetime.now()
    greeting = get_greeting()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d %Y")
    response = (f"The Thousand Sunny is sailing smoothly! {greeting}! "
                f"It is {time_str} on {date_str}. "
                f"Luffy AI is fully powered up and ready to assist!")
    speak_fn(response)
    return response