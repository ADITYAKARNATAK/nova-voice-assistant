# ============================================
# text_to_speech.py — Text To Speech Engine
# Step 5 of Voice Assistant Project
# ============================================

# pyttsx3 is our text-to-speech library
# It works completely OFFLINE — no internet needed
import pyttsx3

# time library lets us add small delays
import time


# ---- FUNCTION: Initialize the TTS Engine ----
def create_engine():
    """
    Creates and configures the text-to-speech engine.
    Returns the configured engine object.
    """

    # Initialize the pyttsx3 engine
    # This starts the speech engine in the background
    engine = pyttsx3.init()

    # ---- Get all available voices on your PC ----
    voices = engine.getProperty('voices')

    # voices[0] = Male voice (default on most Windows PCs)
    # voices[1] = Female voice
    # We will use Female voice for our assistant
    # If you only have one voice, index [0] is fine
    engine.setProperty('voice', voices[1].id)

    # ---- Set the speaking RATE (speed) ----
    # Default is 200 words per minute
    # 150 is slower and clearer — good for an assistant
    engine.setProperty('rate', 150)

    # ---- Set the VOLUME ----
    # Range is 0.0 (silent) to 1.0 (full volume)
    engine.setProperty('volume', 1.0)

    # Return the configured engine
    return engine


# ---- FUNCTION: Speak a given text ----
def speak(text):
    """
    Takes a string of text and speaks it out loud.

    Parameters:
        text (str): The text you want the assistant to say
    """

    # Create a fresh engine each time
    engine = create_engine()

    print("\n" + "-" * 45)
    print(f"  🤖 Assistant: {text}")
    print("-" * 45)

    # say() queues the text to be spoken
    engine.say(text)

    # runAndWait() actually plays the audio
    # It blocks the program until speaking is done
    engine.runAndWait()

    # Small delay after speaking
    # Makes conversation feel more natural
    time.sleep(0.5)


# ---- FUNCTION: Test all voice features ----
def run_test():
    """
    Tests the speak function with different
    types of sentences to make sure everything works
    """

    print("\n" + "🟢 " * 15)
    print("   TEXT TO SPEECH — TEST MODE")
    print("🟢 " * 15)

    # Test 1: Simple greeting
    print("\n  📢 Test 1: Simple Greeting")
    speak("Hello! I am your voice assistant.")

    # Small pause between tests
    time.sleep(1)

    # Test 2: Telling time style
    print("\n  📢 Test 2: Telling Time")
    speak("The current time is 3 30 PM.")

    time.sleep(1)

    # Test 3: Opening website style
    print("\n  📢 Test 3: Opening Website")
    speak("Sure! Opening Google for you right now.")

    time.sleep(1)

    # Test 4: Error message style
    print("\n  📢 Test 4: Error Message")
    speak("Sorry, I did not understand that. Please try again.")

    time.sleep(1)

    # Test 5: Goodbye message
    print("\n  📢 Test 5: Goodbye Message")
    speak("Goodbye! Have a wonderful day. See you soon.")

    print("\n" + "🟢 " * 15)
    print("   ALL TESTS COMPLETE!")
    print("🟢 " * 15 + "\n")


# ---- Run the test ----
if __name__ == "__main__":
    run_test()