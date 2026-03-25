# ============================================
# utils.py — Smart Utility Functions
# Nova Voice Assistant — Final Version
# ============================================

from datetime import datetime
import webbrowser
import random


# ============================================
# SECTION 1: SMART TIME
# ============================================

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
        response += " It's midnight! You should probably sleep."
    elif hour == 12 and now.minute < 5:
        response += " It's noon! Lunchtime!"
    elif 4 <= hour < 6:
        response += " You're up quite early!"
    elif hour >= 23:
        response += " It's quite late. Consider getting some rest!"

    speak_fn(response)
    return response


# ============================================
# SECTION 2: SMART DATE
# ============================================

def tell_date(speak_fn):
    now = datetime.now()
    day_name   = now.strftime("%A")
    month_name = now.strftime("%B")
    day_number = now.strftime("%d")
    year       = now.strftime("%Y")

    response = f"Today is {day_name}, {month_name} {day_number}, {year}."

    if day_name == "Monday":
        response += " Start of the week — let's make it great!"
    elif day_name == "Friday":
        response += " It's Friday! The weekend is almost here!"
    elif day_name in ["Saturday", "Sunday"]:
        response += " It's the weekend! Time to relax."

    if day_number == "01":
        response += f" It's the first of {month_name}!"

    speak_fn(response)
    return response


# ============================================
# SECTION 3: TIME-BASED GREETING
# ============================================

def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"


def greet_user(speak_fn):
    greeting = get_greeting()
    response = f"{greeting}! I am Nova, your personal voice assistant. How can I help you today?"
    speak_fn(response)
    return response


# ============================================
# SECTION 4: JOKES
# ============================================

def tell_joke(speak_fn):
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the programmer quit his job? Because he didn't get arrays!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        "Why do Java developers wear glasses? Because they don't C sharp!",
        "A SQL query walks into a bar and asks two tables: Can I join you?",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
        "Why do Python programmers wear glasses? Because they can't C!",
        "What's a computer's favourite snack? Microchips!"
    ]
    joke = random.choice(jokes)
    speak_fn(joke)
    return joke


# ============================================
# SECTION 5: WEATHER
# ============================================

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
        response = f"Getting weather information for {city}."
        speak_fn(response)
        webbrowser.open(f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}")
    else:
        response = "Getting your local weather information."
        speak_fn(response)
        webbrowser.open("https://www.google.com/search?q=weather+today")
    return response


# ============================================
# SECTION 6: FUN FACTS
# ============================================

def tell_fact(speak_fn):
    facts = [
        "Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs that was still good!",
        "A group of flamingos is called a flamboyance.",
        "Octopuses have three hearts and blue blood.",
        "The first computer bug was an actual bug — a moth found in a Harvard computer in 1947.",
        "Python was named after Monty Python, not the snake!",
        "Bananas are technically berries, but strawberries are not.",
        "A day on Venus is longer than a year on Venus.",
        "There are more possible iterations of a game of chess than atoms in the observable universe."
    ]
    fact = random.choice(facts)
    response = f"Here's an interesting fact: {fact}"
    speak_fn(response)
    return response


# ============================================
# SECTION 7: SYSTEM STATUS
# ============================================

def system_status(speak_fn):
    now = datetime.now()
    greeting = get_greeting()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d %Y")
    response = (f"All systems running perfectly. {greeting}! "
                f"It is {time_str} on {date_str}. "
                f"Nova is ready to assist you!")
    speak_fn(response)
    return response