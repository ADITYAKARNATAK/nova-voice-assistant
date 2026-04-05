# 🏴‍☠️ Luffy AI — Your Pirate AI Assistant

> One Piece themed AI Assistant powered by Google Gemini + Python

---

## 🚀 Live Demo
Deploy on Streamlit Cloud for FREE → See deployment steps below

---

## ⚡ Quick Start

### Web Version (Streamlit)
```bash
pip install streamlit google-generativeai
streamlit run app.py
```

### Terminal Version (with voice)
```bash
# Activate venv first
venv\Scripts\activate

# Install all deps
pip install speechrecognition pyttsx3 pyaudio google-generativeai

# Create config.py from template
copy config.example.py config.py
# Add your API key to config.py

# Run
python assistant.py
```

---

## 🔑 Get FREE Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy it!

---

## ☁️ Deploy to Streamlit Cloud
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repo → set `app.py` as main file
4. Go to **Settings → Secrets** and add:
```toml
GEMINI_API_KEY = "your-actual-key-here"
```
5. Deploy! 🎉

---

## 💬 What Luffy Can Do

| Say This | Luffy Does |
|---|---|
| Anything at all | Gemini AI answers it! |
| `hello` / `hi` | Time-based greeting |
| `what time is it` | Tells current time |
| `what's the date` | Tells today's date |
| `tell me a joke` | Pirate-themed joke |
| `fun fact` | Random interesting fact |
| `explain [anything]` | Gemini explains it |
| `write [anything]` | Gemini writes it |
| `help me with code` | Gemini helps debug |
| `clear` / `reset` | Clears memory |

---

## 📁 Project Files

```
luffy-ai/
├── app.py              ← Web version (Streamlit)
├── assistant.py        ← Terminal + voice version
├── ai_brain.py         ← Gemini AI integration
├── utils.py            ← Time, date, jokes, facts
├── websites.py         ← Website & app commands
├── requirements.txt    ← Web dependencies (2 lines!)
├── config.example.py   ← API key template
├── .gitignore          ← Keeps secrets safe
└── README.md           ← This file
```

---

*🏴‍☠️ "I'm gonna be King of the Pirates — AND the best AI assistant!" — Luffy AI*