# ============================================================
#  app.py — Luffy AI Web App
#  Anime-Style UI — Streamlit Cloud Ready
#  One Piece Themed AI Assistant
# ============================================================

import streamlit as st
import datetime
import random
import os

# ─── Page config — MUST be first Streamlit call ───────────
st.set_page_config(
    page_title="Luffy AI — Your Pirate Assistant",
    page_icon="🏴‍☠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════
# ANIME CSS — One Piece themed dark UI
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;600;700;800&display=swap');

/* ── Root variables ── */
:root {
    --red:      #e63946;
    --gold:     #ffd60a;
    --navy:     #0a0e1a;
    --navy2:    #111827;
    --navy3:    #1a2332;
    --card:     #1e2d3d;
    --card2:    #243447;
    --border:   #2a3f5a;
    --text:     #e8eaf0;
    --dim:      #8899aa;
    --white:    #ffffff;
    --glow-red: 0 0 20px rgba(230,57,70,0.5);
    --glow-gold:0 0 20px rgba(255,214,10,0.4);
}

/* ── Reset & base ── */
* { box-sizing: border-box; }

.stApp {
    background: var(--navy) !important;
    font-family: 'Nunito', sans-serif !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(230,57,70,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(255,214,10,0.04) 0%, transparent 50%),
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 60px,
            rgba(42,63,90,0.15) 60px,
            rgba(42,63,90,0.15) 61px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 60px,
            rgba(42,63,90,0.15) 60px,
            rgba(42,63,90,0.15) 61px
        ) !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Main container ── */
.main .block-container {
    max-width: 780px !important;
    padding: 0 16px 40px 16px !important;
}

/* ── HEADER ── */
.luffy-header {
    text-align: center;
    padding: 32px 20px 20px 20px;
    position: relative;
}

.straw-hat-icon {
    font-size: 72px;
    display: block;
    margin: 0 auto 8px auto;
    filter: drop-shadow(0 0 16px rgba(255,214,10,0.6));
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(-3deg); }
    50%       { transform: translateY(-10px) rotate(3deg); }
}

.luffy-title {
    font-family: 'Bangers', cursive !important;
    font-size: 56px !important;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #ffd60a, #e63946, #ffd60a);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    margin: 0;
    line-height: 1;
    text-shadow: none;
}

@keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.luffy-subtitle {
    font-size: 14px;
    color: var(--dim);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 6px 0 0 0;
    font-weight: 600;
}

.nakama-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(230,57,70,0.2), rgba(255,214,10,0.1));
    border: 1px solid rgba(255,214,10,0.3);
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 12px;
    color: var(--gold);
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 700;
    margin-top: 10px;
}

/* ── Divider ── */
.pirate-divider {
    text-align: center;
    color: var(--border);
    font-size: 18px;
    letter-spacing: 8px;
    margin: 16px 0;
    opacity: 0.6;
}

/* ── API Key Banner ── */
.api-banner {
    background: linear-gradient(135deg, rgba(230,57,70,0.15), rgba(255,214,10,0.08));
    border: 1px solid rgba(230,57,70,0.4);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 0 0 16px 0;
    text-align: center;
    color: #ffb3ba;
    font-size: 14px;
    font-weight: 600;
}

.api-banner a {
    color: var(--gold) !important;
    text-decoration: none;
    font-weight: 700;
}

/* ── Chat area ── */
.chat-area {
    background: var(--navy2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 16px;
    min-height: 420px;
    max-height: 520px;
    overflow-y: auto;
    margin-bottom: 16px;
    scroll-behavior: smooth;
}

.chat-area::-webkit-scrollbar { width: 4px; }
.chat-area::-webkit-scrollbar-track { background: transparent; }
.chat-area::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 2px;
}

/* ── Message bubbles ── */
.msg-row {
    display: flex;
    margin-bottom: 16px;
    animation: fadeUp 0.3s ease;
    align-items: flex-end;
    gap: 10px;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-row.user { flex-direction: row-reverse; }

/* Avatar */
.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
    border: 2px solid var(--border);
}

.avatar.luffy-av {
    background: linear-gradient(135deg, #e63946, #c1121f);
    border-color: var(--red);
    box-shadow: var(--glow-red);
}

.avatar.user-av {
    background: linear-gradient(135deg, #1a4a6b, #0d2137);
    border-color: #2a6090;
}

/* Bubble */
.bubble-wrap { display: flex; flex-direction: column; max-width: 72%; }
.msg-row.user .bubble-wrap { align-items: flex-end; }

.sender-name {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
    padding: 0 4px;
}

.luffy-name { color: var(--red); }
.user-name-label { color: #4d9de0; }

.bubble {
    padding: 12px 16px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.6;
    color: var(--text);
    word-break: break-word;
}

.luffy-bubble {
    background: linear-gradient(135deg, var(--card), var(--card2));
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
}

.user-bubble {
    background: linear-gradient(135deg, #1a3a5c, #0f2540);
    border: 1px solid #2a5080;
    border-bottom-right-radius: 4px;
    text-align: right;
}

.timestamp {
    font-size: 10px;
    color: var(--dim);
    margin-top: 4px;
    padding: 0 4px;
}

/* Thinking bubble */
.thinking-bubble {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    border-bottom-left-radius: 4px;
    padding: 12px 20px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.dot {
    width: 8px;
    height: 8px;
    background: var(--red);
    border-radius: 50%;
    animation: bounce 1.2s ease infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; background: var(--gold); }
.dot:nth-child(3) { animation-delay: 0.4s; background: var(--red); }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40%           { transform: scale(1);   opacity: 1; }
}

/* System message */
.sys-msg {
    text-align: center;
    color: var(--dim);
    font-size: 12px;
    letter-spacing: 1px;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.sys-msg::before, .sys-msg::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Input area ── */
.input-section {
    background: var(--navy2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 14px 16px;
    margin-bottom: 12px;
}

/* Override Streamlit text input */
div[data-testid="stTextInput"] input {
    background: var(--navy3) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    transition: border-color 0.2s !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 2px rgba(230,57,70,0.2) !important;
    outline: none !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: var(--dim) !important;
}

div[data-testid="stTextInput"] label { display: none !important; }

/* Streamlit buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--red), #c1121f) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Bangers', cursive !important;
    font-size: 16px !important;
    letter-spacing: 2px !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(230,57,70,0.3) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(230,57,70,0.5) !important;
}

/* ── Quick commands ── */
.quick-title {
    font-size: 11px;
    color: var(--dim);
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 700;
    margin: 0 0 10px 0;
    text-align: center;
}

.quick-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
}

.quick-btn {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: var(--dim);
    cursor: pointer;
    font-family: 'Nunito', sans-serif;
    font-weight: 600;
    transition: all 0.2s;
    white-space: nowrap;
}

.quick-btn:hover {
    border-color: var(--red);
    color: var(--text);
    background: var(--card2);
}

/* ── Crew stats bar ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 24px;
    padding: 12px 20px;
    background: var(--navy2);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 16px;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-family: 'Bangers', cursive;
    font-size: 22px;
    color: var(--gold);
    line-height: 1;
}

.stat-label {
    font-size: 10px;
    color: var(--dim);
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 700;
}

/* ── Footer ── */
.pirate-footer {
    text-align: center;
    padding: 16px 0 0 0;
    color: var(--dim);
    font-size: 12px;
    letter-spacing: 1px;
}

/* Sidebar override */
.css-1d391kg, [data-testid="stSidebar"] { display: none !important; }

/* Remove streamlit padding */
.css-18e3th9 { padding-top: 0 !important; }
.css-1d391kg { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def get_api_key():
    """Gets API key from Streamlit secrets or environment."""
    # Try Streamlit secrets first
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key and key != "YOUR_GEMINI_API_KEY_HERE":
            return key
    except Exception:
        pass
    # Try environment variable
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
    return ""


@st.cache_resource
def setup_gemini(api_key):
    """Creates Gemini model — cached so it's only created once."""
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "max_output_tokens": 500,
                "temperature"      : 0.85,
            },
            system_instruction="""
You are Luffy, an enthusiastic AI assistant inspired by Monkey D. Luffy from One Piece.
You are helpful, energetic, and friendly — but also genuinely intelligent and knowledgeable.

PERSONALITY RULES:
- Be enthusiastic and positive
- Occasionally use One Piece references naturally (Nakama, Shishishi!, Grand Line, Devil Fruit, Haki, Straw Hat crew)
- Give COMPLETE, ACCURATE answers — never be vague
- Keep responses conversational — no bullet points, no markdown symbols like ** or ##
- For code questions: explain clearly and give working examples
- For factual questions: be accurate and informative
- Maximum 5 sentences unless the question needs a longer answer
- You are LUFFY AI — never say you are Gemini or made by Google
- Be warm and encouraging — every question matters!
- For math/calculations: show the working clearly
            """
        )
        return model
    except Exception as e:
        return None


def ask_gemini(model, question, history):
    """Asks Gemini a question with conversation history."""
    if not model:
        return ("Shishishi! I need my Gemini API key to answer that! "
                "Add GEMINI_API_KEY in Streamlit → Settings → Secrets. "
                "Get a FREE key at aistudio.google.com/app/apikey — it only takes 1 minute, nakama!")
    try:
        # Build conversation history for context
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model",
             "parts": [m["content"]]}
            for m in history[-10:]  # Last 10 messages for context
            if m["role"] in ["user", "luffy"]
        ])
        response = chat.send_message(question)
        answer = response.text.strip()
        # Clean markdown
        for sym in ["**", "__", "##", "# ", "* ", "- "]:
            answer = answer.replace(sym, "")
        return answer
    except Exception as e:
        err = str(e).lower()
        if "api_key" in err or "invalid" in err or "api key" in err:
            return ("My API key has an issue! Make sure GEMINI_API_KEY is correctly set "
                    "in Streamlit secrets. Get a free key at aistudio.google.com/app/apikey!")
        elif "quota" in err or "limit" in err:
            return "I've hit my daily limit! Even pirates need rest. Try again tomorrow nakama!"
        elif "network" in err or "connect" in err:
            return "Can't reach my AI brain right now — check your internet connection nakama!"
        else:
            return f"Something went wrong! Try asking again nakama. Error: {str(e)[:60]}"


def handle_command_web(text, model, history):
    """Routes commands — specific ones first, AI fallback for everything else."""
    t = text.lower().strip()
    now = datetime.datetime.now()

    # ── Time ──
    if "time" in t and "?" in text or t in ["time", "what time", "current time"]:
        return f"Shishishi! It's {now.strftime('%I:%M %p')} right now nakama!"

    if "what time" in t or t.startswith("time"):
        return f"It's {now.strftime('%I:%M %p')} — {'morning' if now.hour < 12 else 'afternoon' if now.hour < 17 else 'evening'} nakama!"

    # ── Date ──
    if "what date" in t or "today's date" in t or t in ["date", "today"]:
        return f"Today is {now.strftime('%A, %B %d, %Y')} — set sail nakama!"

    # ── Greeting ──
    if t in ["hi", "hello", "hey", "howdy", "yo"] or t.startswith("hello") or t.startswith("hi "):
        hour = now.hour
        g = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
        return (f"Shishishi! {g} nakama! I'm Luffy, your AI first mate! "
                f"I've got Gemini AI powers — ask me ANYTHING!")

    # ── How are you ──
    if "how are you" in t or "how r u" in t:
        return "Shishishi! I'm feeling as strong as Gear 5! Ready to answer anything you throw at me nakama!"

    # ── Joke ──
    if "joke" in t or "funny" in t or "make me laugh" in t:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs — and I hate bugs unless they're Sea Kings! Shishishi!",
            "Why did the pirate fail math class? Because he kept confusing X with buried treasure! Shishishi!",
            "How do you organize a pirate party? You planet! No wait... you just say YOHOHOHO!",
            "Why do Python programmers wear glasses? Because they can't C! Get it? Sea? Like the ocean? Shishishi!",
            "What did Zoro say when he got lost? ...I meant to go this way. Shishishi!",
        ]
        return random.choice(jokes)

    # ── Fact ──
    if "fact" in t or "did you know" in t or "tell me something" in t:
        facts = [
            "Shishishi! Honey never spoils — archaeologists found 3000-year-old honey in Egyptian tombs that was still good!",
            "A group of flamingos is called a flamboyance! Even cooler than a pirate crew name, nakama!",
            "Octopuses have THREE hearts and blue blood. Chopper would find that medically fascinating!",
            "Python was named after Monty Python, not the snake! Though Sea Kings are way cooler than both!",
            "There are more possible chess games than atoms in the observable universe — even Zoro would get lost calculating that!",
        ]
        return random.choice(facts)

    # ── Who are you ──
    if "who are you" in t or "your name" in t or "what are you" in t:
        return ("I'm Luffy AI — your AI first mate powered by Google Gemini! "
                "Just like the real Luffy, I never give up on answering your questions! "
                "Ask me ANYTHING nakama — science, code, history, math, creative writing — I've got it all!")

    # ── Who made you ──
    if "who made you" in t or "who built you" in t or "who created you" in t:
        return ("You built me with Python and Streamlit! That makes you the shipwright — like Franky! SUPER! "
                "My AI brain is powered by Google Gemini. Together we're an unstoppable crew nakama!")

    # ── Help ──
    if t in ["help", "what can you do", "commands"] or "what can you" in t:
        return ("Shishishi! I can answer ANY question with my Gemini AI brain! "
                "Ask me about science, history, math, coding, creative writing, or just chat! "
                "I also know the time, date, jokes, and fun facts. Just ask me anything nakama — I never refuse a challenge!")

    # ── Thank you ──
    if "thank" in t or "thanks" in t or "thx" in t:
        return "Shishishi! You're welcome nakama! That's what crewmates are for! 🏴‍☠️"

    # ── Reset ──
    if "reset" in t or "clear" in t or "forget" in t or "new chat" in t:
        return "RESET_CONVERSATION"

    # ── Everything else → Gemini AI ──
    return ask_gemini(model, text, history)


def get_greeting():
    h = datetime.datetime.now().hour
    if 5 <= h < 12:  return "Good morning, nakama"
    elif 12 <= h < 17: return "Good afternoon, nakama"
    elif 17 <= h < 21: return "Good evening, nakama"
    else:              return "Good night, nakama"


def format_time():
    return datetime.datetime.now().strftime("%I:%M %p")


# ═══════════════════════════════════════════════════════════
# STREAMLIT SESSION STATE INIT
# ═══════════════════════════════════════════════════════════

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.msg_count = 0

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""


# ═══════════════════════════════════════════════════════════
# SETUP GEMINI
# ═══════════════════════════════════════════════════════════

api_key = get_api_key()
model   = setup_gemini(api_key)


# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════

st.markdown("""
<div class="luffy-header">
    <span class="straw-hat-icon">🎩</span>
    <h1 class="luffy-title">LUFFY AI</h1>
    <p class="luffy-subtitle">Your AI First Mate · Powered by Gemini</p>
    <span class="nakama-badge">🏴‍☠️ Straw Hat Crew AI · Always Ready</span>
</div>
<div class="pirate-divider">⚓ ✦ ⚓ ✦ ⚓</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# API KEY WARNING (if missing)
# ═══════════════════════════════════════════════════════════

if not api_key:
    st.markdown("""
    <div class="api-banner">
        ⚠️ <strong>No API Key Detected!</strong>
        Luffy needs his Gemini Devil Fruit powers!<br>
        Go to <strong>Streamlit → Settings → Secrets</strong> and add:<br>
        <code style="background:rgba(0,0,0,0.3); padding:3px 8px; border-radius:4px; color:#ffd60a;">
        GEMINI_API_KEY = "your-key-here"</code><br>
        Get your FREE key at
        <a href="https://aistudio.google.com/app/apikey" target="_blank">
        aistudio.google.com/app/apikey</a>
        — takes 60 seconds! 🏴‍☠️
    </div>
    """, unsafe_allow_html=True)
else:
    # Connected badge
    st.markdown("""
    <div style="text-align:center; margin-bottom:16px;">
        <span style="background:rgba(52,168,83,0.15); border:1px solid rgba(52,168,83,0.4);
                     border-radius:20px; padding:5px 16px; font-size:12px;
                     color:#4ade80; font-weight:700; letter-spacing:1px;">
            ✅ GEMINI AI CONNECTED — ASK ME ANYTHING!
        </span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# STATS BAR
# ═══════════════════════════════════════════════════════════

st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-value">{st.session_state.msg_count}</div>
        <div class="stat-label">Messages</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">{'✅' if api_key else '❌'}</div>
        <div class="stat-label">AI Status</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">{format_time()}</div>
        <div class="stat-label">Ship Time</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">∞</div>
        <div class="stat-label">Questions</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# CHAT DISPLAY
# ═══════════════════════════════════════════════════════════

# Build chat HTML
chat_html = '<div class="chat-area" id="chatArea">'

if not st.session_state.messages:
    # Welcome message
    now_str = format_time()
    greeting = get_greeting()
    welcome = (f"Shishishi! {greeting}! I'm Luffy, your AI first mate! "
               f"I'm powered by Google Gemini, so I can answer ANYTHING you ask — "
               f"science, math, code, history, creative writing, you name it! "
               f"Let's set sail nakama! 🏴‍☠️")
    chat_html += f"""
    <div class="msg-row">
        <div class="avatar luffy-av">🎩</div>
        <div class="bubble-wrap">
            <div class="sender-name luffy-name">LUFFY AI</div>
            <div class="bubble luffy-bubble">{welcome}</div>
            <div class="timestamp">{now_str}</div>
        </div>
    </div>
    """

for msg in st.session_state.messages:
    if msg["role"] == "system":
        chat_html += f'<div class="sys-msg">{msg["content"]}</div>'
    elif msg["role"] == "luffy":
        chat_html += f"""
        <div class="msg-row">
            <div class="avatar luffy-av">🎩</div>
            <div class="bubble-wrap">
                <div class="sender-name luffy-name">LUFFY AI</div>
                <div class="bubble luffy-bubble">{msg["content"]}</div>
                <div class="timestamp">{msg.get("time", "")}</div>
            </div>
        </div>
        """
    elif msg["role"] == "user":
        chat_html += f"""
        <div class="msg-row user">
            <div class="avatar user-av">👤</div>
            <div class="bubble-wrap">
                <div class="sender-name user-name-label">YOU</div>
                <div class="bubble user-bubble">{msg["content"]}</div>
                <div class="timestamp">{msg.get("time", "")}</div>
            </div>
        </div>
        """

chat_html += "</div>"

# Auto-scroll JS
chat_html += """
<script>
    setTimeout(function() {
        var el = document.getElementById('chatArea');
        if (el) el.scrollTop = el.scrollHeight;
    }, 100);
</script>
"""

st.markdown(chat_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# QUICK COMMAND BUTTONS
# ═══════════════════════════════════════════════════════════

st.markdown('<p class="quick-title">⚡ Quick Commands</p>', unsafe_allow_html=True)

quick_commands = [
    "What time is it?", "Tell me a joke", "Fun fact",
    "What can you do?", "Explain Python", "What is AI?",
]

cols = st.columns(len(quick_commands))
for i, cmd in enumerate(quick_commands):
    with cols[i]:
        if st.button(cmd, key=f"quick_{i}"):
            st.session_state.pending_input = cmd


# ═══════════════════════════════════════════════════════════
# INPUT AREA
# ═══════════════════════════════════════════════════════════

st.markdown('<div class="input-section">', unsafe_allow_html=True)

col_in, col_btn = st.columns([5, 1])

with col_in:
    user_text = st.text_input(
        label="msg",
        placeholder="Ask me anything, nakama... 🏴‍☠️",
        label_visibility="collapsed",
        key=f"chat_input_{st.session_state.input_key}",
        value=st.session_state.pending_input
    )

with col_btn:
    send_clicked = st.button("SEND ➤", key="send_btn")

st.markdown("</div>", unsafe_allow_html=True)

# Clear button row
c1, c2, c3 = st.columns([3, 2, 3])
with c2:
    if st.button("🗑️ Clear Voyage Log", key="clear_btn"):
        st.session_state.messages = []
        st.session_state.msg_count = 0
        st.session_state.input_key += 1
        st.session_state.pending_input = ""
        st.rerun()


# ═══════════════════════════════════════════════════════════
# PROCESS INPUT
# ═══════════════════════════════════════════════════════════

# Determine what to process
to_process = ""
if send_clicked and user_text and user_text.strip():
    to_process = user_text.strip()
elif st.session_state.pending_input and not send_clicked:
    to_process = st.session_state.pending_input

if to_process:
    # Reset pending
    st.session_state.pending_input = ""

    # Add user message
    ts = datetime.datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({
        "role": "user",
        "content": to_process,
        "time": ts
    })
    st.session_state.msg_count += 1

    # Get Luffy's response
    with st.spinner("🏴‍☠️ Luffy is powering up..."):
        response = handle_command_web(
            to_process,
            model,
            st.session_state.messages
        )

    # Handle reset command
    if response == "RESET_CONVERSATION":
        st.session_state.messages = [{
            "role": "system",
            "content": "⚓ Voyage log cleared — new adventure begins!"
        }]
        st.session_state.messages.append({
            "role": "luffy",
            "content": "Shishishi! Memory cleared! Fresh start — what's our next adventure nakama?",
            "time": ts
        })
        st.session_state.msg_count = 1
    else:
        st.session_state.messages.append({
            "role": "luffy",
            "content": response,
            "time": ts
        })
        st.session_state.msg_count += 1

    # Clear input and rerun
    st.session_state.input_key += 1
    st.rerun()


# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════

st.markdown("""
<div class="pirate-divider" style="margin-top:8px;">⚓ ✦ ⚓ ✦ ⚓</div>
<div class="pirate-footer">
    🏴‍☠️ Built with Python · Streamlit · Google Gemini AI<br>
    <span style="color:#ffd60a; font-weight:700;">"I'm gonna be King of the Pirates — AND the best AI assistant!"</span>
    — Luffy AI
</div>
""", unsafe_allow_html=True)