# ============================================================
#
#   🏴‍☠️  LUFFY AI — TERMINAL VERSION  🏴‍☠️
#   Your AI First Mate — Powered by Gemini
#   One Piece themed Voice + Text Assistant
#
# ============================================================

from datetime import datetime
import time, os
import speech_recognition as sr
import pyttsx3

from utils    import (tell_time, tell_date, greet_user, tell_joke,
                      tell_weather, tell_fact, system_status, get_greeting)
from websites import open_website, open_app, handle_search
from ai_brain import ask_luffy, reset_conversation

ASSISTANT_NAME = "Luffy"
LANGUAGE       = "en-in"
SPEECH_RATE    = 160
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
    print(f"\n  {'─'*50}")
    print(f"  🏴‍☠️  {ASSISTANT_NAME}: {text}")
    print(f"  {'─'*50}")
    try:
        engine = create_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass
    time.sleep(0.3)


def listen():
    recognizer = sr.Recognizer()
    for attempt in range(1, MAX_RETRIES + 1):
        with sr.Microphone() as source:
            print(f"\n  {'═'*50}")
            print(f"  🎤  {ASSISTANT_NAME} is Listening..." +
                  (f" (Attempt {attempt}/{MAX_RETRIES})" if attempt > 1 else ""))
            print(f"  {'═'*50}")
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
                    speak("Shishishi! I couldn't catch that. Say it again nakama!")
            except sr.RequestError:
                speak("Network error! Check your internet, nakama!")
                return None
            except sr.WaitTimeoutError:
                print("  ⏰ No speech detected.")
                if attempt == MAX_RETRIES:
                    speak("I didn't hear you! Try again nakama!")
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

    exit_words = ["exit", "quit", "bye", "goodbye", "stop", "see you"]
    if any(w in text for w in exit_words):
        speak("Shishishi! Bye nakama! I'll become King of the Pirates — AND the best AI assistant!")
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
        speak("Shishishi! I'm doing amazing! Strong as ever! How can I help you nakama?")
    elif "your name" in text or "who are you" in text:
        speak("I'm Luffy! Your AI first mate! I'm gonna be King of the Pirates AND answer all your questions!")
    elif "joke" in text:
        tell_joke(speak_fn)
    elif "fact" in text:
        tell_fact(speak_fn)
    elif "status" in text or "are you there" in text:
        system_status(speak_fn)
    elif "reset" in text or "forget" in text or "clear memory" in text:
        msg = reset_conversation()
        speak(msg)
    elif "who made you" in text or "who built you" in text:
        speak("You built me with Python and Gemini AI! That makes you the shipwright — like Franky! SUPER!")
    elif "thank" in text:
        speak("Shishishi! You're welcome nakama! That's what crewmates are for!")
    elif "help" in text or "what can you do" in text:
        speak("I can answer ANY question with my Gemini AI brain, tell the time and date, "
              "open websites and apps, search Google and YouTube, check weather, "
              "tell jokes and facts! Just ask me anything nakama!")
    else:
        # AI fallback — ask Gemini
        print(f"  🧠 Asking Gemini AI...")
        response = ask_luffy(text)
        speak(response)

    return True


def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    now = datetime.now()
    print("\n")
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║                                                  ║")
    print("  ║         🏴‍☠️   LUFFY AI ASSISTANT   🏴‍☠️           ║")
    print("  ║                                                  ║")
    print("  ║    ⠀⠀⠀⠀🎩  Straw Hat Crew AI  🎩⠀⠀⠀⠀         ║")
    print("  ║         Powered by Gemini + Python               ║")
    print("  ║                                                  ║")
    print(f"  ║   📅  {now.strftime('%A, %B %d %Y'):<42}║")
    print(f"  ║   🕐  {now.strftime('%I:%M %p'):<42}║")
    print("  ╠══════════════════════════════════════════════════╣")
    print("  ║                                                  ║")
    print("  ║   💬  COMMANDS (or just ask ANYTHING!):          ║")
    print("  ║                                                  ║")
    print("  ║   • hello / hi              • what's the time   ║")
    print("  ║   • what's the date         • weather in [city] ║")
    print("  ║   • open google/youtube/... • open notepad/...  ║")
    print("  ║   • search for [anything]   • tell me a joke    ║")
    print("  ║   • tell me a fact          • clear memory      ║")
    print("  ║   • ANY QUESTION → Gemini AI answers it!        ║")
    print("  ║   • exit / bye                                   ║")
    print("  ║                                                  ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print()


def main():
    show_banner()
    greeting = get_greeting()
    speak(f"{greeting}! I'm Luffy, your AI first mate! "
          f"Ask me ANYTHING — I've got Gemini AI powers! "
          f"Let's set sail nakama!")

    silence_count = 0

    while True:
        user_input = listen()

        if user_input is None:
            silence_count += 1
            if silence_count >= MAX_SILENCE:
                speak("Shishishi! You still there nakama? I'm here whenever you need me!")
                silence_count = 0
            time.sleep(1)
            continue

        silence_count = 0
        keep_running = handle_command(user_input)

        if not keep_running:
            print("\n  ╔══════════════════════════════════════╗")
            print(f"  ║  🏴‍☠️  {ASSISTANT_NAME} has set sail. Farewell!  ║")
            print("  ╚══════════════════════════════════════╝\n")
            break

        time.sleep(1)


if __name__ == "__main__":
    main()