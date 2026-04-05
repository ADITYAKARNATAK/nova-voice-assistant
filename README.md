# 🏴‍☠️ Luffy AI — Personal AI Assistant

> One Piece themed AI Assistant · Google Gemini · Python · Streamlit

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to https://streamlit.io/cloud → New App
3. Select your repo, branch `main`, file `app.py`
4. Click **Settings → Secrets** and add:
```toml
GEMINI_API_KEY = "your-actual-gemini-key-here"
```
5. Click Deploy!

**Get FREE Gemini key:** https://aistudio.google.com/app/apikey

---

## 💻 Run Locally

### Web version
```bash
pip install streamlit google-generativeai pytz
streamlit run app.py
```

### Terminal + Voice version
```bash
# Activate venv
venv\Scripts\activate

# Install
pip install speechrecognition pyttsx3 pyaudio google-generativeai pytz

# Setup API key
copy config.example.py config.py
# Edit config.py and add your key

# Run
python assistant.py
```

---

## 📁 Files

| File | Purpose |
|---|---|
| `app.py` | Web app (Streamlit) — deploy this |
| `assistant.py` | Terminal + voice version |
| `ai_brain.py` | Gemini AI integration |
| `utils.py` | Time (IST), jokes, facts |
| `websites.py` | Website & app commands |
| `requirements.txt` | Streamlit Cloud dependencies |
| `config.example.py` | API key template |

---

*🏴‍☠️ "I'm going to be the greatest AI assistant!" — Luffy AI*