# ============================================================
#  assistant.py — Luffy AI Terminal + Voice Version
#  Model: gemini-2.0-flash · IST Time
# ============================================================

from datetime import datetime, timedelta
import time, os
import speech_recognition as sr
import pyttsx3

try:
    import pytz
    IST = pytz.timezone("Asia/Kolkata")
    def now_ist(): return datetime.now(IST)
except ImportError:
    def now_ist(): return datetime.utcnow() + timedelta(hours=5, minutes=30)

from utils    import (tell_time, tell_date, greet_user, tell_joke,
                      tell_weather, tell_fact, system_status, get_greeting)
from websites import open_website, open_app, handle_search
from ai_brain import ask_luffy, reset_conversation

ASSISTANT_NAME = "Luffy"
LANGUAGE       = "en-in"
SPEECH_RATE    = 155
LISTEN_TIMEOUT = 5
MAX_RETRIES    = 3


def create_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    try:    engine.setProperty('voice', voices[1].id)
    except: engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', SPEECH_RATE)
    engine.setProperty('volume', 1.0)
    return engine

def speak(text):
    print(f"\n  {'─'*54}")
    print(f"  🏴‍☠️  {ASSISTANT_NAME}: {text}")
    print(f"  {'─'*54}")
    try:
        e = create_engine(); e.say(text); e.runAndWait()
    except: pass
    time.sleep(0.3)

def listen():
    rec = sr.Recognizer()
    for attempt in range(1, MAX_RETRIES + 1):
        with sr.Microphone() as src:
            print(f"\n  {'═'*54}")
            print(f"  🎤  Listening..." +
                  (f" (Attempt {attempt}/{MAX_RETRIES})" if attempt > 1 else ""))
            print(f"  {'═'*54}")
            rec.adjust_for_ambient_noise(src, duration=1)
            try:
                audio = rec.listen(src, timeout=LISTEN_TIMEOUT, phrase_time_limit=10)
                print("  ⏳ Processing...")
                text = rec.recognize_google(audio, language=LANGUAGE).lower().strip()
                print(f"  ✅ Heard: '{text}'")
                return text
            except sr.UnknownValueError:
                print("  ❌ Could not understand.")
                if attempt == MAX_RETRIES:
                    speak("I couldn't understand that. Could you say it again?")
            except sr.RequestError:
                speak("Network error. Please check your internet connection.")
                return None
            except sr.WaitTimeoutError:
                print("  ⏰ No speech detected.")
                if attempt == MAX_RETRIES:
                    speak("I didn't hear anything. Please try again.")
            except Exception as e:
                print(f"  ⚠️ {e}"); return None
            time.sleep(0.3)
    return None

def handle_command(text):
    if not text: return True
    s = lambda m: speak(m)
    t = text.lower()

    if any(w in t for w in ["exit","quit","bye","goodbye","stop"]):
        speak("Goodbye! Come back anytime. 🏴‍☠️")
        return False

    matched, _ = open_website(t, s)
    if matched: return True
    matched, _ = open_app(t, s)
    if matched: return True
    matched, _ = handle_search(t, s)
    if matched: return True

    if any(p in t for p in ["what time","time is it","current time"]):
        tell_time(s)
    elif "date" in t or "today" in t:
        tell_date(s)
    elif "weather" in t:
        tell_weather(t, s)
    elif any(w in t for w in ["hello","hi","hey"]):
        greet_user(s)
    elif "how are you" in t:
        speak("I'm doing great and fully powered up! How can I help?")
    elif "your name" in t or "who are you" in t:
        speak("I'm Luffy AI — your personal AI assistant powered by Gemini 2.0! Ask me anything.")
    elif "joke" in t:
        tell_joke(s)
    elif "fact" in t:
        tell_fact(s)
    elif "status" in t:
        system_status(s)
    elif "reset" in t or "clear" in t:
        speak(reset_conversation())
    elif "who made you" in t or "who built you" in t:
        speak("You built me with Python and Gemini 2.0! Great work!")
    elif "thank" in t:
        speak("You're welcome! Happy to help anytime.")
    elif "help" in t or "what can you do" in t:
        speak("I can answer any question, tell the time and date in IST, "
              "open websites and apps, search the web, and much more. Just ask!")
    else:
        print(f"  🧠 Asking Gemini 2.0...")
        speak(ask_luffy(text))

    return True

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    n = now_ist()
    print("\n")
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║                                                      ║")
    print("  ║      🎩  LUFFY AI — TERMINAL ASSISTANT  🎩          ║")
    print("  ║      Gemini 2.0 Flash · Python · IST Time            ║")
    print("  ║                                                      ║")
    print(f"  ║   📅  {n.strftime('%A, %B %d, %Y'):<46}║")
    print(f"  ║   🕐  {n.strftime('%I:%M %p IST'):<46}║")
    print("  ╠══════════════════════════════════════════════════════╣")
    print("  ║   Ask me ANYTHING — Gemini 2.0 answers it all!       ║")
    print("  ║   hello · time · date · weather · open · search      ║")
    print("  ║   joke · fact · help · bye                           ║")
    print("  ╚══════════════════════════════════════════════════════╝\n")

def main():
    show_banner()
    speak(f"{get_greeting()}! I'm Luffy AI. Ask me anything!")
    silence = 0
    while True:
        inp = listen()
        if inp is None:
            silence += 1
            if silence >= 3:
                speak("Still there? Ready whenever you are!")
                silence = 0
            time.sleep(1)
            continue
        silence = 0
        if not handle_command(inp):
            print("\n  🏴‍☠️  Luffy AI stopped. Goodbye!\n")
            break
        time.sleep(1)

if __name__ == "__main__":
    main()