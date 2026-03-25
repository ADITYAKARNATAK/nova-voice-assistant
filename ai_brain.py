# ============================================
# ai_brain.py — Gemini AI Integration
# Nova Voice Assistant
# This gives Nova the ability to answer
# ANY question intelligently!
# ============================================

# Google's Gemini AI library
import google.generativeai as genai

# Import our config settings
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    SYSTEM_PROMPT,
    ASSISTANT_NAME
)


# ============================================
# SETUP GEMINI
# ============================================

# Configure the library with our API key
genai.configure(api_key=GEMINI_API_KEY)

# Create the model with our settings
model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    generation_config={
        # max_output_tokens limits response length
        # Keeps Nova's answers short and speakable
        "max_output_tokens" : MAX_TOKENS,

        # temperature controls creativity
        # 0.0 = very factual, 1.0 = very creative
        "temperature"       : TEMPERATURE,
    },
    # system_instruction sets Nova's personality
    system_instruction=SYSTEM_PROMPT
)

# Start a chat session
# chat history allows Nova to remember
# what was said earlier in conversation!
chat_session = model.start_chat(history=[])


# ============================================
# ASK GEMINI FUNCTION
# ============================================

def ask_gemini(question):
    """
    Sends a question to Gemini AI and returns
    the response as a clean string.

    Parameters:
        question (str): The user's question

    Returns:
        str: Nova's intelligent response
    """

    try:
        # Send message to Gemini
        # chat_session.send_message() maintains
        # conversation history automatically!
        response = chat_session.send_message(question)

        # Extract the text from response
        answer = response.text.strip()

        # Clean up any markdown symbols Gemini might add
        # These sound weird when spoken aloud
        answer = answer.replace("*", "")
        answer = answer.replace("#", "")
        answer = answer.replace("`", "")
        answer = answer.replace("**", "")
        answer = answer.replace("__", "")
        answer = answer.replace("\n\n", ". ")
        answer = answer.replace("\n", ". ")

        return answer

    except Exception as e:
        error_msg = str(e)

        # Handle specific API errors gracefully
        if "API_KEY" in error_msg or "api key" in error_msg.lower():
            return "My API key seems invalid. Please check config.py and add a valid Gemini API key."

        elif "quota" in error_msg.lower():
            return "I have reached my daily question limit. Please try again tomorrow."

        elif "network" in error_msg.lower() or "connect" in error_msg.lower():
            return "I cannot connect to my AI brain right now. Please check your internet."

        else:
            return f"Something went wrong with my AI brain. Please try again."


# ============================================
# RESET CONVERSATION
# ============================================

def reset_conversation():
    """
    Clears the chat history so Nova starts
    a fresh conversation with no memory.
    """
    global chat_session
    chat_session = model.start_chat(history=[])
    return "Conversation history cleared. Starting fresh!"


# ============================================
# TEST FUNCTION
# ============================================

def test_gemini():
    """
    Quick test to verify Gemini is working.
    Run this file directly to test.
    """
    print("\n" + "🟣 " * 15)
    print("   GEMINI AI — TEST MODE")
    print("🟣 " * 15)

    test_questions = [
        "What is Python programming in one sentence?",
        "Tell me a fun fact about space.",
        "What did I just ask you first?"   # Tests memory!
    ]

    for q in test_questions:
        print(f"\n  ❓ Question: {q}")
        answer = ask_gemini(q)
        print(f"  🤖 Nova: {answer}")

    print("\n" + "🟣 " * 15)
    print("   TEST COMPLETE!")
    print("🟣 " * 15 + "\n")


if __name__ == "__main__":
    test_gemini()