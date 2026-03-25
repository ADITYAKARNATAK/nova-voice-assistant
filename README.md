# 🤖 Nova — Personal AI Voice Assistant



---

## 🚀 Quick Start

### 1. Create & Activate Virtual Environment
```bash
python -m venv venv --without-pip
venv\Scripts\activate
python -m ensurepip
python -m pip install --upgrade pip
```

### 2. Install Dependencies
```bash
pip install speechrecognition pyttsx3 pyaudio
```
> If pyaudio fails: `pip install pipwin` then `pipwin install pyaudio`

### 3. Run Nova

**GUI Mode (Recommended — Gemini Style):**
```bash
python nova_gui.py
```

**Terminal Mode:**
```bash
python assistant.py
```

---

## 💬 Voice Commands

| Command | What Nova Does |
|---|---|
| `hello / hi / hey` | Greets you based on time of day |
| `what's the time` | Tells current time naturally |
| `what's the date` | Tells today's date with context |
| `weather in Mumbai` | Opens Google weather for that city |
| `open google` | Opens Google in browser |
| `open youtube` | Opens YouTube |
| `open gmail` | Opens Gmail |
| `open whatsapp` | Opens WhatsApp Web |
| `open netflix` | Opens Netflix |
| `open instagram` | Opens Instagram |
| `open notepad` | Opens Windows Notepad |
| `open calculator` | Opens Windows Calculator |
| `open paint` | Opens MS Paint |
| `search for python tutorials` | Searches Google |
| `search youtube for lofi music` | Searches YouTube |
| `wikipedia machine learning` | Searches Wikipedia |
| `tell me a joke` | Tells a programmer joke |
| `tell me a fact` | Tells a fun fact |
| `what can you do` | Lists all commands |
| `exit / bye / quit` | Shuts down Nova |

---

## 📁 Project Structure

```
voice_assistant/
├── nova_gui.py        ← GUI version (run this!)
├── assistant.py       ← Terminal version
├── utils.py           ← Time, date, jokes, facts
├── websites.py        ← Website & app commands
├── requirements.txt   ← Dependencies
└── README.md          ← This file
```

---

## ⚙️ Configuration

Open `nova_gui.py` and edit the top section:

```python
ASSISTANT_NAME = "Nova"     # Change assistant name
LANGUAGE       = "en-in"    # en-in / en-us / en-gb
SPEECH_RATE    = 150        # Speaking speed
LISTEN_TIMEOUT = 6          # Seconds to wait for speech
MAX_RETRIES    = 3          # Retry attempts on failure
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| Mic not detected | Check Windows Sound → Input device |
| PyAudio install fails | Use `pipwin install pyaudio` |
| Can't understand speech | Speak clearly, check internet |
| No voice output | Check speaker / Windows volume |
| `ModuleNotFoundError` | Make sure venv is activated |

---

## 🏗️ Built With

- `speechrecognition` — Voice to text
- `pyttsx3` — Text to voice  
- `pyaudio` — Microphone access
- `tkinter` — GUI framework
- `datetime` — Time and date
- `webbrowser` — Open websites
- `os` — Open Windows apps

---

*Built with ❤️ using Python*