# ============================================
# speech_to_text.py — Speech To Text Engine
# Step 4 of Voice Assistant Project
# ============================================

# speech_recognition library handles all mic input
import speech_recognition as sr


# ---- FUNCTION: Listen and Convert Speech to Text ----
def listen_and_convert():
    """
    This function:
    1. Opens the microphone
    2. Listens for your voice
    3. Converts speech to text
    4. Returns the text as a string
    """

    # Create a Recognizer object
    # Think of this as the 'brain' that processes audio
    recognizer = sr.Recognizer()

    # Open the microphone as our audio source
    with sr.Microphone() as source:

        # --- Console UI ---
        print("\n" + "=" * 45)
        print("        🎤  LISTENING...  🎤")
        print("=" * 45)
        print("  Speak now! I'm ready to hear you.\n")

        # Adjust for background noise automatically
        # duration=1 means 1 second of noise calibration
        # Keeps it fast but accurate
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            # listen() captures your voice
            # timeout=5 → stops waiting after 5 seconds of silence
            # phrase_time_limit=10 → max 10 seconds of speaking
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            print("  ⏳ Processing your speech...\n")

            # recognize_google() converts audio to text
            # language="en-in" means Indian English accent
            # Change to "en-us" for American English
            # Change to "en-gb" for British English
            text = recognizer.recognize_google(audio, language="en-in")

            # .lower() converts text to lowercase
            # So "Hello" and "hello" are treated the same
            text = text.lower()

            print(f"  ✅ You said: '{text}'")
            print("=" * 45)

            # Return the recognized text to whoever called this function
            return text

        # Error 1: Could not understand what was said
        except sr.UnknownValueError:
            print("  ❌ Sorry, I could not understand.")
            print("     Please speak clearly and try again.")
            print("=" * 45)
            # Return None so the calling code knows it failed
            return None

        # Error 2: No internet or Google API issue
        except sr.RequestError as e:
            print(f"  ❌ API Error: {e}")
            print("     Check your internet connection.")
            print("=" * 45)
            return None

        # Error 3: You didn't speak within 5 seconds
        except sr.WaitTimeoutError:
            print("  ⏰ Timeout! No speech detected.")
            print("     Please try again.")
            print("=" * 45)
            return None


# ---- FUNCTION: Test the speech to text ----
def run_test():
    """
    Test function that runs speech to text
    3 times so we can verify it works reliably
    """

    print("\n" + "🔵 " * 15)
    print("   SPEECH TO TEXT — TEST MODE")
    print("🔵 " * 15)
    print("\n  We will test 3 times.")
    print("  Speak something each time!\n")

    # Loop 3 times to test reliability
    for i in range(1, 4):

        print(f"\n  --- TEST {i} of 3 ---")

        # Call our listen function
        result = listen_and_convert()

        # Check what came back
        if result:
            print(f"\n  📝 Captured Text  : '{result}'")
            print(f"  📏 Word Count     : {len(result.split())} words")
            print(f"  🔡 Character Count: {len(result)} characters")
        else:
            print("\n  ⚠️  No text captured this time.")

    print("\n" + "🔵 " * 15)
    print("   TEST COMPLETE!")
    print("🔵 " * 15 + "\n")


# ---- Run the test ----
if __name__ == "__main__":
    run_test()


