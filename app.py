# ============================================================
#  app.py — Luffy AI Web App — FINAL ULTIMATE VERSION
#  Uses st.chat_message (no raw HTML bugs)
#  Indian Standard Time (IST)
#  Normal helpful responses + One Piece theme
# ============================================================

import streamlit as st
import datetime
import random
import os
import pytz  # For Indian Standard Time

# ── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="Luffy AI — Your Pirate Assistant",
    page_icon="🏴‍☠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Indian Standard Time helper ───────────────────────────
IST = pytz.timezone("Asia/Kolkata")

def now_ist():
    """Returns current datetime in Indian Standard Time."""
    return datetime.datetime.now(IST)

def time_str():
    return now_ist().strftime("%I:%M %p IST")

def date_str():
    return now_ist().strftime("%A, %B %d, %Y")

def greeting():
    h = now_ist().hour
    if 5 <= h < 12:  return "Good morning"
    elif 12 <= h < 17: return "Good afternoon"
    elif 17 <= h < 21: return "Good evening"
    else:              return "Good night"

# ── CSS — One Piece Anime Dark Theme ─────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --red:    #e63946;
    --gold:   #ffd60a;
    --navy:   #0a0e1a;
    --navy2:  #111827;
    --card:   #1e2d3d;
    --border: #2a3f5a;
    --text:   #e8eaf0;
    --dim:    #8899aa;
}

/* Base */
.stApp {
    background: var(--navy) !important;
    font-family: 'Nunito', sans-serif !important;
    background-image:
        radial-gradient(ellipse at 15% 15%, rgba(230,57,70,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 85%, rgba(255,214,10,0.05) 0%, transparent 50%) !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton, [data-testid="stToolbar"] { display: none !important; }

/* Main container */
.main .block-container {
    max-width: 800px !important;
    padding: 0 20px 60px 20px !important;
}

/* ── HEADER ── */
.luffy-header {
    text-align: center;
    padding: 28px 0 8px 0;
}
.hat-icon {
    font-size: 64px;
    display: block;
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 0 18px rgba(255,214,10,0.7));
}
@keyframes float {
    0%,100% { transform: translateY(0) rotate(-4deg); }
    50%      { transform: translateY(-10px) rotate(4deg); }
}
.main-title {
    font-family: 'Bangers', cursive !important;
    font-size: 58px !important;
    letter-spacing: 5px !important;
    background: linear-gradient(135deg, #ffd60a 0%, #e63946 50%, #ffd60a 100%);
    background-size: 200% auto;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: shine 3s linear infinite;
    margin: 0 !important; line-height: 1 !important;
}
@keyframes shine {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.sub-title {
    color: var(--dim);
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 700;
    margin: 6px 0 10px 0;
}
.status-badge {
    display: inline-block;
    border-radius: 20px;
    padding: 5px 18px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.connected {
    background: rgba(52,168,83,0.15);
    border: 1px solid rgba(52,168,83,0.5);
    color: #4ade80;
}
.disconnected {
    background: rgba(230,57,70,0.15);
    border: 1px solid rgba(230,57,70,0.5);
    color: #ff6b6b;
}

/* ── STATS ── */
.stats-row {
    display: flex;
    justify-content: center;
    gap: 0;
    background: var(--navy2);
    border: 1px solid var(--border);
    border-radius: 14px;
    margin: 14px 0;
    overflow: hidden;
}
.stat-cell {
    flex: 1;
    text-align: center;
    padding: 12px 8px;
    border-right: 1px solid var(--border);
}
.stat-cell:last-child { border-right: none; }
.stat-val {
    font-family: 'Bangers', cursive;
    font-size: 20px;
    color: var(--gold);
    display: block;
    line-height: 1.2;
}
.stat-lbl {
    font-size: 9px;
    color: var(--dim);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 700;
    display: block;
}

/* ── API WARNING ── */
.api-warn {
    background: rgba(230,57,70,0.12);
    border: 1px solid rgba(230,57,70,0.4);
    border-radius: 12px;
    padding: 14px 18px;
    color: #ffb3ba;
    font-size: 13px;
    font-weight: 600;
    text-align: center;
    margin: 10px 0;
    line-height: 1.7;
}
.api-warn code {
    background: rgba(0,0,0,0.4);
    padding: 2px 8px;
    border-radius: 4px;
    color: var(--gold);
    font-size: 12px;
}
.api-warn a { color: var(--gold) !important; font-weight: 700; }

/* ── CHAT MESSAGES — override Streamlit defaults ── */
[data-testid="stChatMessage"] {
    background: var(--navy2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessage"] p {
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.65 !important;
    margin: 0 !important;
}
/* User message different color */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(26, 58, 92, 0.6) !important;
    border-color: #2a5080 !important;
}

/* ── INPUT ── */
[data-testid="stChatInput"] {
    background: var(--navy2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--navy2) !important;
    color: var(--text) !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--dim) !important;
}
[data-testid="stChatInput"] button {
    background: var(--red) !important;
    border-radius: 8px !important;
}

/* ── QUICK BUTTONS ── */
.stButton > button {
    background: var(--card) !important;
    color: var(--dim) !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    padding: 6px 12px !important;
    transition: all 0.2s !important;
    white-space: nowrap !important;
    width: 100% !important;
}
.stButton > button:hover {
    border-color: var(--red) !important;
    color: var(--text) !important;
    background: rgba(230,57,70,0.1) !important;
}

/* Clear button */
.clear-btn > button {
    background: transparent !important;
    border-color: var(--border) !important;
    color: var(--dim) !important;
    font-size: 11px !important;
    padding: 4px 12px !important;
}

/* ── DIVIDER ── */
.divider {
    text-align: center;
    color: var(--border);
    font-size: 16px;
    letter-spacing: 8px;
    margin: 10px 0;
    opacity: 0.5;
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    color: var(--dim);
    font-size: 11px;
    letter-spacing: 1px;
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid var(--border);
}
.footer strong { color: var(--gold); }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# GEMINI SETUP
# ═══════════════════════════════════════════════════════════

def get_api_key():
    """Gets API key — tries Streamlit secrets then env variable."""
    try:
        k = st.secrets.get("GEMINI_API_KEY", "")
        if k and k != "YOUR_GEMINI_API_KEY_HERE":
            return k
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "")


@st.cache_resource
def load_model(api_key: str):
    """Loads Gemini model once and caches it."""
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "max_output_tokens": 600,
                "temperature":       0.75,
            },
            system_instruction="""
You are Luffy AI, a helpful and enthusiastic AI assistant.
Your personality is inspired by Monkey D. Luffy from One Piece — you are energetic, positive, brave, and never give up.

STRICT RULES:
1. Give COMPLETE, ACCURATE, HELPFUL answers — never be vague or refuse reasonable questions
2. Write in plain readable text — NO markdown symbols like **, ##, *, -
3. Keep responses conversational — like talking to a smart friend
4. For code: write clean working code with brief explanation
5. For math: show the calculation clearly and give the answer
6. For facts: be accurate and informative
7. Keep responses to 3-5 sentences unless the topic needs more detail
8. You are LUFFY AI — never say you are Gemini or made by Google
9. Occasionally add ONE short enthusiastic phrase like "Let's go!" or "That's awesome!" naturally
10. ALWAYS answer the question — never say you cannot help

IMPORTANT: Do NOT use Nakama excessively. Talk normally like a helpful assistant with a fun personality.
            """
        )
    except Exception:
        return None


def ask_ai(model, question: str, history: list) -> str:
    """Sends question to Gemini with conversation history."""
    if not model:
        return (
            "I need my Gemini API key to answer that! "
            "Please add GEMINI_API_KEY in Streamlit → Manage App → Settings → Secrets. "
            "Get a FREE key in 60 seconds at: aistudio.google.com/app/apikey"
        )
    try:
        # Build history for context (last 8 exchanges)
        chat_history = []
        for m in history[-16:]:
            if m["role"] == "user":
                chat_history.append({"role": "user",   "parts": [m["content"]]})
            elif m["role"] == "assistant":
                chat_history.append({"role": "model",  "parts": [m["content"]]})

        chat = model.start_chat(history=chat_history)
        resp = chat.send_message(question)
        answer = resp.text.strip()

        # Clean any accidental markdown
        for sym in ["**", "__", "```", "##", "# "]:
            answer = answer.replace(sym, "")

        return answer

    except Exception as e:
        err = str(e).lower()
        if "api_key" in err or "invalid" in err or "key" in err:
            return "My API key seems incorrect. Check that GEMINI_API_KEY is set correctly in Streamlit secrets."
        elif "quota" in err or "limit" in err:
            return "I've hit today's usage limit! Try again tomorrow or check your Gemini API quota."
        elif "network" in err or "connect" in err:
            return "Network error — please check your internet connection and try again."
        elif "safety" in err or "block" in err:
            return "I can't answer that particular question, but I'm happy to help with anything else!"
        else:
            return f"Something went wrong. Please try again! (Error: {str(e)[:80]})"


# ═══════════════════════════════════════════════════════════
# COMMAND HANDLER — Specific commands first, AI fallback
# ═══════════════════════════════════════════════════════════

def handle(text: str, model, history: list) -> str:
    """Routes the user's message to the right handler."""
    t = text.lower().strip()

    # ── Time (IST) ──────────────────────────────────────────
    if any(p in t for p in ["what time", "current time", "time now", "time is it", "what's the time"]):
        n = now_ist()
        h = n.hour
        period = "morning" if h < 12 else "afternoon" if h < 17 else "evening" if h < 21 else "night"
        return f"It's {n.strftime('%I:%M %p')} IST ({period}). Hope your day is going great!"

    # ── Date ────────────────────────────────────────────────
    if any(p in t for p in ["what date", "today's date", "what day", "today is", "current date"]) or t in ["date", "today"]:
        n = now_ist()
        days_map = {"Monday": "Start of the week!", "Friday": "Almost weekend!", "Saturday": "Weekend!", "Sunday": "Sunday funday!"}
        extra = days_map.get(n.strftime("%A"), "")
        return f"Today is {n.strftime('%A, %B %d, %Y')}. {extra}"

    # ── Greeting ─────────────────────────────────────────────
    if t in ["hi", "hello", "hey", "yo", "hiya"] or t.startswith(("hi ", "hello ", "hey ")):
        return (f"{greeting()}! I'm Luffy AI, your personal assistant with the power of Google Gemini! "
                f"I can answer any question — science, math, coding, history, creative writing, and much more. What's on your mind?")

    # ── How are you ──────────────────────────────────────────
    if any(p in t for p in ["how are you", "how r u", "how do you do", "you okay", "you good"]):
        return "I'm doing great, fully powered up and ready to help! What can I do for you today?"

    # ── Joke ─────────────────────────────────────────────────
    if any(p in t for p in ["tell me a joke", "joke", "make me laugh", "funny"]):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            "Why did the developer go broke? Because he used up all his cache!",
            "How many programmers does it take to change a light bulb? None — that's a hardware problem!",
            "Why do Python developers wear glasses? Because they can't C!",
            "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
            "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
            "What's a pirate's favorite programming language? Arrr-duino! 🏴‍☠️",
        ]
        return random.choice(jokes)

    # ── Fun fact ─────────────────────────────────────────────
    if any(p in t for p in ["fun fact", "tell me a fact", "random fact", "did you know", "interesting fact"]):
        facts = [
            "Honey never spoils — archaeologists found 3,000-year-old honey in Egyptian tombs that was still perfectly edible!",
            "A group of flamingos is called a 'flamboyance'. One of the best animal group names ever!",
            "Octopuses have three hearts, two pump blood to the gills and one pumps it to the rest of the body.",
            "The first computer bug was a literal bug — an actual moth found trapped in a Harvard computer relay in 1947!",
            "Python was named after Monty Python's Flying Circus, not the snake.",
            "There are more possible iterations of a game of chess than there are atoms in the observable universe.",
            "Bananas are technically berries, but strawberries are not actually berries botanically.",
            "The human brain uses about 20% of the body's total energy despite being only 2% of body weight.",
        ]
        return random.choice(facts)

    # ── Who are you ──────────────────────────────────────────
    if any(p in t for p in ["who are you", "what are you", "your name", "introduce yourself", "about you"]):
        return (
            "I'm Luffy AI — a powerful AI assistant built with Python and Google Gemini! "
            "I can answer virtually any question you throw at me: science, history, math, coding, "
            "creative writing, analysis, and much more. "
            "Think of me as your personal AI first mate, always ready to help. What would you like to know?"
        )

    # ── Who made you ─────────────────────────────────────────
    if any(p in t for p in ["who made you", "who built you", "who created you", "who made this"]):
        return (
            "I was built using Python and Streamlit by you! "
            "My intelligence comes from Google Gemini AI. "
            "It's a great project — you should be proud of building this!"
        )

    # ── Thank you ────────────────────────────────────────────
    if any(p in t for p in ["thank you", "thanks", "thx", "ty", "thank u"]):
        return "You're welcome! Happy to help anytime. Feel free to ask me anything else!"

    # ── Help / capabilities ──────────────────────────────────
    if any(p in t for p in ["help", "what can you do", "capabilities", "commands", "features"]):
        return (
            "I can help you with almost anything! Here's what I'm great at: "
            "Answering general knowledge questions, explaining complex topics simply, "
            "helping with math and calculations, writing and debugging code, "
            "creative writing and storytelling, giving advice and suggestions, "
            "current time and date in IST, jokes, fun facts, and much more. "
            "Just ask me anything and I'll do my best to help!"
        )

    # ── Clear ────────────────────────────────────────────────
    if any(p in t for p in ["clear", "reset", "new chat", "start over", "forget"]):
        return "CLEAR_CHAT"

    # ── Goodbye ──────────────────────────────────────────────
    if any(p in t for p in ["bye", "goodbye", "see you", "later", "exit"]):
        return "Goodbye! It was great chatting with you. Come back anytime you need help! 🏴‍☠️"

    # ── Everything else → Gemini AI ──────────────────────────
    return ask_ai(model, text, history)


# ═══════════════════════════════════════════════════════════
# SESSION STATE INIT
# ═══════════════════════════════════════════════════════════

if "messages" not in st.session_state:
    st.session_state.messages = []
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

api_key = get_api_key()
model   = load_model(api_key)


# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════

st.markdown(f"""
<div class="luffy-header">
    <span class="hat-icon">🎩</span>
    <div class="main-title">LUFFY AI</div>
    <div class="sub-title">Your Personal AI Assistant · One Piece Edition</div>
    <span class="status-badge {'connected' if api_key else 'disconnected'}">
        {'✅ Gemini AI Online — Ask Me Anything!' if api_key else '❌ API Key Missing — Setup Required'}
    </span>
</div>
<div class="divider">⚓ ✦ ⚓ ✦ ⚓</div>
""", unsafe_allow_html=True)


# ── API Warning ───────────────────────────────────────────
if not api_key:
    st.markdown("""
    <div class="api-warn">
        ⚠️ <strong>Gemini API Key Not Found!</strong><br>
        Go to <strong>Streamlit → Manage App → Settings → Secrets</strong> and add:<br>
        <code>GEMINI_API_KEY = "your-key-here"</code><br>
        Get your FREE key at
        <a href="https://aistudio.google.com/app/apikey" target="_blank">
            aistudio.google.com/app/apikey
        </a> — takes under 60 seconds!
    </div>
    """, unsafe_allow_html=True)


# ── Stats bar ─────────────────────────────────────────────
n = now_ist()
st.markdown(f"""
<div class="stats-row">
    <div class="stat-cell">
        <span class="stat-val">{st.session_state.msg_count}</span>
        <span class="stat-lbl">Messages</span>
    </div>
    <div class="stat-cell">
        <span class="stat-val">{'✅' if api_key else '❌'}</span>
        <span class="stat-lbl">AI Status</span>
    </div>
    <div class="stat-cell">
        <span class="stat-val">{n.strftime('%I:%M %p')}</span>
        <span class="stat-lbl">IST Time</span>
    </div>
    <div class="stat-cell">
        <span class="stat-val">{n.strftime('%d %b')}</span>
        <span class="stat-lbl">Date</span>
    </div>
    <div class="stat-cell">
        <span class="stat-val">∞</span>
        <span class="stat-lbl">Questions</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# CHAT HISTORY — using st.chat_message (NO raw HTML bugs!)
# ═══════════════════════════════════════════════════════════

# Welcome message on first load
if not st.session_state.messages:
    welcome = (
        f"{greeting()}! I'm Luffy AI, your personal AI assistant powered by Google Gemini. "
        f"I can answer questions on any topic — science, math, coding, history, creative writing, and more. "
        f"The current time in India is {n.strftime('%I:%M %p IST')}. "
        f"What would you like to know today?"
    )
    with st.chat_message("assistant", avatar="🎩"):
        st.write(welcome)

# Display chat history
for msg in st.session_state.messages:
    role   = msg["role"]      # "user" or "assistant"
    avatar = "🎩" if role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
        st.write(msg["content"])
        if msg.get("time"):
            st.caption(msg["time"])


# ═══════════════════════════════════════════════════════════
# QUICK COMMAND BUTTONS
# ═══════════════════════════════════════════════════════════

st.markdown('<p style="text-align:center; color:#8899aa; font-size:11px; letter-spacing:2px; text-transform:uppercase; font-weight:700; margin: 12px 0 8px 0;">⚡ Quick Commands</p>', unsafe_allow_html=True)

quick = [
    "What time is it?",
    "Tell me a joke",
    "Fun fact",
    "What can you do?",
    "Explain Python",
    "What is AI?",
]

cols = st.columns(len(quick))
triggered = None
for i, cmd in enumerate(quick):
    with cols[i]:
        if st.button(cmd, key=f"q{i}"):
            triggered = cmd


# ═══════════════════════════════════════════════════════════
# CHAT INPUT — st.chat_input (proper Streamlit component)
# ═══════════════════════════════════════════════════════════

user_input = st.chat_input("Ask me anything... 🏴‍☠️")

# Use quick button if clicked, otherwise use typed input
to_process = triggered or user_input

if to_process:
    ts = now_ist().strftime("%I:%M %p IST")

    # Show user message immediately
    with st.chat_message("user", avatar="👤"):
        st.write(to_process)

    # Save user message
    st.session_state.messages.append({
        "role":    "user",
        "content": to_process,
        "time":    ts
    })
    st.session_state.msg_count += 1

    # Get response
    with st.chat_message("assistant", avatar="🎩"):
        with st.spinner("Thinking..."):
            response = handle(to_process, model, st.session_state.messages)

        if response == "CLEAR_CHAT":
            st.session_state.messages = []
            st.session_state.msg_count = 0
            st.write("Chat cleared! Ready for a fresh start. What would you like to know?")
            st.rerun()
        else:
            st.write(response)
            st.caption(ts)

    # Save assistant message
    if response != "CLEAR_CHAT":
        st.session_state.messages.append({
            "role":    "assistant",
            "content": response,
            "time":    ts
        })
        st.session_state.msg_count += 1


# ── Clear button ──────────────────────────────────────────
st.markdown("")
c1, c2, c3 = st.columns([3, 2, 3])
with c2:
    with st.container():
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", key="clear"):
            st.session_state.messages = []
            st.session_state.msg_count = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────
st.markdown("""
<div class="divider" style="margin-top:16px;">⚓ ✦ ⚓ ✦ ⚓</div>
<div class="footer">
    Built with Python · Streamlit · Google Gemini AI<br>
    <strong>"I'm going to be the greatest AI assistant!" — Luffy AI 🏴‍☠️</strong>
</div>
""", unsafe_allow_html=True)