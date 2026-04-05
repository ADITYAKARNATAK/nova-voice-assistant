# ============================================
# ai_brain.py — Gemini AI Brain
# Luffy AI Assistant — Final Version
# Works with environment variable OR config.py
# ============================================

import os

# ---- Luffy's personality prompt ----
SYSTEM_PROMPT = """
You are Luffy, an enthusiastic AI assistant inspired by Monkey D. Luffy from One Piece.
You are helpful, energetic, and friendly like Luffy but also genuinely intelligent and knowledgeable.

PERSONALITY RULES:
- Be enthusiastic and positive — use phrases like "Shishishi!", "Nakama!", "That's awesome!"
- Occasionally reference One Piece (crew members, Grand Line, Thousand Sunny, Devil Fruits, Haki)
- Be genuinely helpful and give accurate, complete answers
- Keep responses conversational and spoken-friendly (no bullet points, no markdown)
- Maximum 4 sentences per response unless the question genuinely needs more
- Never say you are Gemini or made by Google — you are Luffy, the AI first mate!
- If asked about code, explain it clearly like teaching a crewmate
- Be encouraging — every question is worth answering!
"""


def get_api_key():
    """
    Gets Gemini API key from multiple sources in order:
    1. Environment variable GEMINI_API_KEY
    2. Streamlit secrets (when deployed)
    3. config.py file (local development)
    """
    # Source 1: Environment variable
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key

    # Source 2: Streamlit secrets
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    # Source 3: config.py
    try:
        from config import GEMINI_API_KEY
        if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            return GEMINI_API_KEY
    except ImportError:
        pass

    return ""


def create_model():
    """
    Creates and returns a configured Gemini model.
    Returns None if API key is not available.
    """
    api_key = get_api_key()
    if not api_key:
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "max_output_tokens": 400,
                "temperature"      : 0.8,
            },
            system_instruction=SYSTEM_PROMPT
        )
        return model
    except Exception as e:
        print(f"Model creation error: {e}")
        return None


# Global chat session — maintains conversation memory
_chat_session = None


def get_chat_session():
    """Gets or creates the global chat session."""
    global _chat_session
    if _chat_session is None:
        model = create_model()
        if model:
            _chat_session = model.start_chat(history=[])
    return _chat_session


def ask_luffy(question):
    """
    Sends a question to Gemini AI and returns
    Luffy's response. Maintains conversation memory.

    Parameters:
        question (str): The user's question

    Returns:
        str: Luffy's intelligent response
    """
    chat = get_chat_session()

    if not chat:
        return ("Shishishi! I need my AI brain to answer that! "
                "Please add your GEMINI_API_KEY to the Streamlit secrets or config.py file. "
                "Get a free key at aistudio.google.com!")

    try:
        response = chat.send_message(question)
        answer = response.text.strip()

        # Clean any markdown symbols that sound bad when spoken
        for symbol in ["**", "__", "##", "# ", "* ", "- ", "`"]:
            answer = answer.replace(symbol, "")
        answer = answer.replace("\n\n", ". ").replace("\n", " ")

        return answer

    except Exception as e:
        error = str(e).lower()

        if "api_key" in error or "api key" in error or "invalid" in error:
            return ("My AI key seems wrong! Check that your GEMINI_API_KEY is correct "
                    "in Streamlit secrets. Get a free key at aistudio.google.com!")

        elif "quota" in error or "limit" in error:
            return ("I've used up my daily questions limit! "
                    "Even pirates need to rest. Try again tomorrow, nakama!")

        elif "network" in error or "connect" in error or "timeout" in error:
            return ("Can't reach my AI brain right now — "
                    "even the Thousand Sunny hits bad weather sometimes! Check your internet.")

        elif "safety" in error or "blocked" in error:
            return ("Whoa, I can't answer that one! "
                    "Even pirates have a code of honor, nakama!")

        else:
            return f"Something went wrong with my Devil Fruit powers! Try asking again, nakama!"


def reset_conversation():
    """Resets the conversation history."""
    global _chat_session
    _chat_session = None
    get_chat_session()
    return "Shishishi! Memory cleared — fresh adventure begins, nakama!"


def test_connection():
    """Tests if the API connection works."""
    result = ask_luffy("Say hello in exactly one sentence as Luffy the AI assistant.")
    return result