# ============================================
# command_handler.py — The Brain of Assistant
# Step 6 of Voice Assistant Project
# ============================================

# datetime lets us get current time and date
from datetime import datetime

# webbrowser lets us open websites
import webbrowser

# os lets us interact with the operating system
import os

# Import our speak function from step 5
# This lets us reuse code we already wrote!
from text_to_speech import speak


# ============================================
# COMMAND HANDLER FUNCTION
# ============================================

def handle_command(text):
    """
    Takes recognized text as input.
    Matches it to a command.
    Executes the correct action.

    Parameters:
        text (str): The lowercased text from speech recognition

    Returns:
        bool: False if assistant should exit, True otherwise
    """

    # Safety check — if no text came in, do nothing
    if text is None:
        speak("I didn't catch that. Could you please repeat?")
        return True


    # ============================================
    # COMMAND 1: GREETING
    # Triggers: "hello", "hi", "hey"
    # ============================================
    if "hello" in text or "hi" in text or "hey" in text:
        speak("Hello! I am your voice assistant. How can I help you today?")


    # ============================================
    # COMMAND 2: HOW ARE YOU
    # Triggers: "how are you"
    # ============================================
    elif "how are you" in text:
        speak("I am doing great! Thank you for asking. How can I assist you?")


    # ============================================
    # COMMAND 3: WHAT IS YOUR NAME
    # Triggers: "your name", "what are you called"
    # ============================================
    elif "your name" in text or "what are you called" in text:
        speak("My name is Nova. Your personal voice assistant!")


    # ============================================
    # COMMAND 4: TELL TIME
    # Triggers: "time"
    # ============================================
    elif "time" in text:

        # Get current time using datetime
        # strftime formats the time as: Hour:Minute AM/PM
        current_time = datetime.now().strftime("%I:%M %p")

        speak(f"The current time is {current_time}")


    # ============================================
    # COMMAND 5: TELL DATE
    # Triggers: "date", "today", "day"
    # ============================================
    elif "date" in text or "today" in text or "day" in text:

        # Format: Monday, January 01 2025
        current_date = datetime.now().strftime("%A, %B %d %Y")

        speak(f"Today is {current_date}")


    # ============================================
    # COMMAND 6: OPEN GOOGLE
    # Triggers: "open google", "google"
    # ============================================
    elif "google" in text:
        speak("Sure! Opening Google for you.")

        # webbrowser.open() opens the URL in default browser
        webbrowser.open("https://www.google.com")


    # ============================================
    # COMMAND 7: OPEN YOUTUBE
    # Triggers: "open youtube", "youtube"
    # ============================================
    elif "youtube" in text:
        speak("Opening YouTube right away!")
        webbrowser.open("https://www.youtube.com")


    # ============================================
    # COMMAND 8: OPEN GITHUB
    # Triggers: "github"
    # ============================================
    elif "github" in text:
        speak("Opening GitHub for you.")
        webbrowser.open("https://www.github.com")


    # ============================================
    # COMMAND 9: SEARCH GOOGLE
    # Triggers: "search for ...", "search ..."
    # ============================================
    elif "search" in text:

        # Remove the word "search" and "for" from the text
        # Whatever is left becomes the search query
        query = text.replace("search for", "").replace("search", "").strip()

        if query:
            speak(f"Searching Google for {query}")

            # f-string builds the Google search URL
            # + replaces spaces in the query with +
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        else:
            speak("What would you like me to search for?")


    # ============================================
    # COMMAND 10: EXIT / QUIT
    # Triggers: "exit", "quit", "bye", "goodbye"
    # ============================================
    elif "exit" in text or "quit" in text or "bye" in text or "goodbye" in text:
        speak("Goodbye! Have a great day. See you soon!")

        # Returning False signals the main loop to STOP
        return False


    # ============================================
    # DEFAULT: Command Not Recognized
    # ============================================
    else:
        speak(f"Sorry, I don't know how to handle that yet. You said: {text}")


    # Return True means keep the assistant running
    return True


# ============================================
# TEST THE COMMAND HANDLER
# ============================================

def run_test():
    """
    Tests the command handler with fake text inputs
    so we don't need to use the mic every time
    """

    print("\n" + "🟡 " * 15)
    print("   COMMAND HANDLER — TEST MODE")
    print("🟡 " * 15)
    print("\n  Testing commands with fake text input...\n")

    # List of fake commands to test
    # These simulate what speech recognition would return
    test_commands = [
        "hello",
        "how are you",
        "what is your name",
        "what is the time",
        "what is the date",
        "open google",
        "open youtube",
        "search for python tutorials",
        "i want to exit"
    ]

    # Loop through each fake command
    for command in test_commands:
        print(f"\n  🧪 Testing command: '{command}'")

        # Send it to the handler
        result = handle_command(command)

        # If result is False, assistant wants to exit
        if not result:
            print("\n  🛑 Exit command received. Stopping test.")
            break

    print("\n" + "🟡 " * 15)
    print("   TEST COMPLETE!")
    print("🟡 " * 15 + "\n")


# ---- Run the test ----
if __name__ == "__main__":
    run_test()
