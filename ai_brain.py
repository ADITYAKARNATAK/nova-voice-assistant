# ai_brain.py — Gemini AI Brain (Terminal Version)
# Model: gemini-2.0-flash — best free model 2025
import os

SYSTEM_PROMPT = """
You are Luffy AI, a helpful and enthusiastic AI assistant.
Always give COMPLETE, ACCURATE, HELPFUL answers.
Write in plain text — no markdown symbols like **, ##, *, or ```.
Be conversational and friendly.
Keep casual answers to 3-5 sentences; technical/detailed questions can be longer.
You are LUFFY AI — never say you are Gemini or Google.
Never refuse a reasonable question.
"""

_chat = None

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
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
        if not key:
            return None
        try:
            import google.generativeai as genai
            genai.configure(api_key=key)
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",   # ✅ Best free model
                generation_config={
                    "max_output_tokens": 600,
                    "temperature":       0.7,
                    "top_p":             0.95,
                },
                system_instruction=SYSTEM_PROMPT
            )
            _chat = model.start_chat(history=[])
        except Exception as e:
            print(f"Gemini setup error: {e}")
            return None
    return _chat

def ask_luffy(question):
    chat = get_chat()
    if not chat:
        return ("I need a Gemini API key to answer that! "
                "Add GEMINI_API_KEY to config.py. "
                "Get a free key at aistudio.google.com/app/apikey")
    try:
        resp   = chat.send_message(question)
        answer = resp.text.strip()
        for s in ["**", "__", "##", "# ", "```"]:
            answer = answer.replace(s, "")
        return answer
    except Exception as e:
        err = str(e).lower()
        if "quota" in err or "429" in err:
            return "Usage limit reached. Please try again in a few minutes."
        elif "404" in err or "not found" in err:
            return "Model error. Please check your internet connection and try again."
        return f"Error: {str(e)[:100]}. Please try again."

def reset_conversation():
    global _chat
    _chat = None
    get_chat()
    return "Conversation cleared! Fresh start!"