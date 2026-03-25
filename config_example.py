# ============================================
# config.example.py — Template for config.py
# Copy this file, rename it to config.py
# and fill in your own API keys
# ============================================

# Get your FREE Gemini API key at:
# https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# ---- Assistant Settings ----
ASSISTANT_NAME  = "Nova"
LANGUAGE        = "en-in"
SPEECH_RATE     = 150
SPEECH_VOLUME   = 1.0
LISTEN_TIMEOUT  = 6
MAX_RETRIES     = 3

# ---- Gemini Settings ----
GEMINI_MODEL    = "gemini-1.5-flash"
MAX_TOKENS      = 300
TEMPERATURE     = 0.7

SYSTEM_PROMPT = """
You are Nova, a helpful personal AI voice assistant.
Keep ALL responses under 3 sentences.
Never use bullet points or markdown symbols.
Speak naturally as if talking out loud.
"""