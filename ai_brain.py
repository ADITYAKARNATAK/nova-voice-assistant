# ai_brain.py — Gemini AI Brain (Terminal Version)
import os

SYSTEM_PROMPT = """
You are Luffy AI, a helpful and enthusiastic AI assistant.
Give COMPLETE, ACCURATE, HELPFUL answers.
Write in plain text — no markdown symbols like **, ##, *.
Be conversational and friendly. Keep responses to 3-5 sentences unless more is needed.
You are Luffy AI — never say you are Gemini or Google.
"""

_chat = None

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY", "")
    if key: return key
    try:
        from config import GEMINI_API_KEY
        if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            return GEMINI_API_KEY
    except ImportError:
        pass
    return ""

def get_chat():
    global _chat
    if _chat is None:
        key = get_api_key()
        if not key: return None
        try:
            import google.generativeai as genai
            genai.configure(api_key=key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={"max_output_tokens": 400, "temperature": 0.75},
                system_instruction=SYSTEM_PROMPT
            )
            _chat = model.start_chat(history=[])
        except Exception as e:
            print(f"Gemini error: {e}")
            return None
    return _chat

def ask_luffy(question):
    chat = get_chat()
    if not chat:
        return ("I need a Gemini API key! Add it to config.py. "
                "Get a free key at aistudio.google.com/app/apikey")
    try:
        resp = chat.send_message(question)
        answer = resp.text.strip()
        for s in ["**", "__", "##", "# ", "```"]:
            answer = answer.replace(s, "")
        return answer
    except Exception as e:
        return f"Error: {str(e)[:100]}. Please try again."

def reset_conversation():
    global _chat
    _chat = None
    get_chat()
    return "Conversation cleared! Fresh start!"