# # ============================================
# # test_mic.py — Test Microphone Input
# # Step 3 of Voice Assistant Project
# # ============================================

# # Import the speech recognition library
# import speech_recognition as sr

# # ---- FUNCTION: Test Microphone ----
# def test_microphone():

#     # Create a Recognizer object
#     # This is the brain that will process audio
#     recognizer = sr.Recognizer()

#     # sr.Microphone() accesses your default system microphone
#     with sr.Microphone() as source:

#         print("=" * 40)
#         print("   MICROPHONE TEST STARTED")
#         print("=" * 40)
#         print("\n🎤 Adjusting for background noise...")
#         print("   Please stay quiet for 2 seconds...\n")

#         # This line listens to background noise
#         # and adjusts sensitivity automatically
#         # duration=2 means it listens for 2 seconds
#         recognizer.adjust_for_ambient_noise(source, duration=2)

#         print("✅ Noise adjustment done!")
#         print("\n🗣️  Now SPEAK something into your mic...")
#         print("   (Say anything like 'Hello' or 'Testing')\n")

#         # listen() captures audio from the microphone
#         # It waits until you speak and stops when you pause
#         audio = recognizer.listen(source)

#         print("⏳ Got your audio! Processing...\n")

#     # Try to convert the audio to text
#     try:

#         # recognize_google() sends audio to Google's
#         # free speech-to-text API and returns a string
#         text = recognizer.recognize_google(audio)

#         print("=" * 40)
#         print("   MICROPHONE TEST RESULT")
#         print("=" * 40)
#         print(f"\n✅ SUCCESS! You said: '{text}'")
#         print("\n🎉 Your microphone is working perfectly!")
#         print("=" * 40)

#     # This error means Google couldn't understand the audio
#     except sr.UnknownValueError:
#         print("❌ Could not understand audio.")
#         print("   Try speaking louder and more clearly.")

#     # This error means there's no internet connection
#     # Google API needs internet to work
#     except sr.RequestError as e:
#         print(f"❌ Internet/API error: {e}")
#         print("   Make sure you are connected to the internet.")

# # ---- Run the function ----
# if __name__ == "__main__":
#     test_microphone()