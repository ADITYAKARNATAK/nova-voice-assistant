# ============================================================
#
#   ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗
#   ████╗  ██║██╔═══██╗██║   ██║██╔══██╗
#   ██╔██╗ ██║██║   ██║██║   ██║███████║
#   ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
#   ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
#   ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝
#
#   Nova — Terminal Voice Assistant
#   Final Clean Version (No GUI)
#   Run this if you prefer terminal mode.
#
# ============================================================

from datetime import datetime
import time, os
import speech_recognition as sr
import pyttsx3
from utils import (tell_time, tell_date, greet_user, tell_joke,
                   tell_weather, tell_fact, system_status, get_greeting)
from websites import open_website, open_app, handle_search

ASSISTANT_NAME = "Nova"
LANGUAGE       = "en-in"
SPEECH_RATE    = 150
LISTEN_TIMEOUT = 5
MAX_RETRIES    = 3
MAX_SILENCE    = 3


def create_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    try:
        engine.setProperty('voice', voices[1].id)
    except IndexError:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', SPEECH_RATE)
    engine.setProperty('volume', 1.0)
    return engine


def speak(text):
    print(f"\n  {'─'*46}\n  🤖 {ASSISTANT_NAME}: {text}\n  {'─'*46}")
    engine = create_engine()
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)


def listen():
    recognizer = sr.Recognizer()
    for attempt in range(1, MAX_RETRIES + 1):
        with sr.Microphone() as source:
            print(f"\n  {'═'*46}")
            print(f"  🎤  {ASSISTANT_NAME} is Listening..." +
                  (f" (Attempt {attempt}/{MAX_RETRIES})" if attempt > 1 else ""))
            print(f"  {'═'*46}")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=10)
                print("  ⏳ Processing...")
                text = recognizer.recognize_google(audio, language=LANGUAGE).lower().strip()
                print(f"  ✅ Heard: '{text}'")
                return text
            except sr.UnknownValueError:
                print("  ❌ Could not understand.")
                if attempt == MAX_RETRIES:
                    speak("Sorry, I couldn't understand. Please try again.")
            except sr.RequestError:
                speak("Network error. Check your internet.")
                return None
            except sr.WaitTimeoutError:
                print("  ⏰ No speech detected.")
                if attempt == MAX_RETRIES:
                    speak("I didn't hear anything. Please try again.")
            except Exception as e:
                print(f"  ⚠️ Error: {e}")
                return None
            time.sleep(0.3)
    return None


def handle_command(text):
    if text is None:
        return True

    def speak_fn(msg):
        speak(msg)

    exit_words = ["exit", "quit", "bye", "goodbye", "stop", "shut down"]
    if any(w in text for w in exit_words):
        speak("Goodbye! Have a wonderful day. See you soon!")
        return False

    matched, _ = open_website(text, speak_fn)
    if matched: return True
    matched, _ = open_app(text, speak_fn)
    if matched: return True
    matched, _ = handle_search(text, speak_fn)
    if matched: return True

    if "time" in text:
        tell_time(speak_fn)
    elif "date" in text or "today" in text:
        tell_date(speak_fn)
    elif "weather" in text:
        tell_weather(text, speak_fn)
    elif any(w in text for w in ["hello", "hi", "hey"]):
        greet_user(speak_fn)
    elif "how are you" in text:
        speak("I'm running perfectly! How can I help?")
    elif "your name" in text or "who are you" in text:
        speak(f"I am {ASSISTANT_NAME}, your personal AI voice assistant!")
    elif "joke" in text:
        tell_joke(speak_fn)
    elif "fact" in text:
        tell_fact(speak_fn)
    elif "status" in text:
        system_status(speak_fn)
    elif "who made you" in text or "who built you" in text:
        speak("You built me with Python! You should be proud.")
    elif "thank" in text:
        speak("You're welcome! Always here to help.")
    elif "help" in text or "what can you do" in text:
        speak("I can tell the time and date, open websites and apps, "
              "search Google, YouTube, Wikipedia, check weather, "
              "tell jokes and facts. Just ask!")
    else:
        speak(f"I'm not sure how to help with that. Say 'help' to see what I can do!")

    return True


def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    now = datetime.now()
    print("\n")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║   Nova — Terminal Voice Assistant            ║")
    print("  ║   Version 2.0  |  Built with Python          ║")
    print(f"  ║   📅  {now.strftime('%A, %B %d %Y'):<38}║")
    print(f"  ║   🕐  {now.strftime('%I:%M %p'):<38}║")
    print("  ╠══════════════════════════════════════════════╣")
    print("  ║  hello • time • date • weather in [city]     ║")
    print("  ║  open google/youtube/gmail/netflix/...        ║")
    print("  ║  open notepad/calculator/paint/...            ║")
    print("  ║  search for • search youtube for              ║")
    print("  ║  wikipedia • joke • fact • help • bye         ║")
    print("  ╚══════════════════════════════════════════════╝\n")


def main():
    show_banner()
    greeting = get_greeting()
    speak(f"{greeting}! I am {ASSISTANT_NAME}. Ready to help — what can I do for you?")

    silence_count = 0

    while True:
        user_input = listen()

        if user_input is None:
            silence_count += 1
            if silence_count >= MAX_SILENCE:
                speak("Are you still there? I'm here whenever you need me!")
                silence_count = 0
            time.sleep(1)
            continue

        silence_count = 0
        keep_running = handle_command(user_input)

        if not keep_running:
            print("\n  ╔══════════════════════════════╗")
            print(f"  ║  👋  {ASSISTANT_NAME} stopped. Goodbye!   ║")
            print("  ╚══════════════════════════════╝\n")
            break

        time.sleep(1)


if __name__ == "__main__":
    main()