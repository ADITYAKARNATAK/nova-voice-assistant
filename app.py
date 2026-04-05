# ============================================================
#  app.py — Luffy AI Web App — FINAL v3
#  Model: gemini-2.0-flash (best free model)
#  IST Time · Normal responses · No HTML bugs
# ============================================================

import streamlit as st
import datetime
import random
import os

st.set_page_config(
    page_title="Luffy AI — Your Pirate Assistant",
    page_icon="🏴‍☠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Indian Standard Time ───────────────────────────────────
try:
    import pytz
    IST = pytz.timezone("Asia/Kolkata")
    def now_ist():
        return datetime.datetime.now(IST)
except ImportError:
    # fallback if pytz not available
    def now_ist():
        return datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)

def time_str():
    return now_ist().strftime("%I:%M %p IST")

def date_str():
    return now_ist().strftime("%A, %B %d, %Y")

def greeting():
    h = now_ist().hour
    if 5  <= h < 12: return "Good morning"
    elif 12 <= h < 17: return "Good afternoon"
    elif 17 <= h < 21: return "Good evening"
    else:              return "Good night"

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --red:    #e63946;
    --gold:   #ffd60a;
    --navy:   #0a0e1a;
    --navy2:  #111827;
    --navy3:  #1a2535;
    --card:   #1e2d3d;
    --border: #2a3f5a;
    --text:   #e8eaf0;
    --dim:    #8899aa;
}

.stApp {
    background: var(--navy) !important;
    font-family: 'Nunito', sans-serif !important;
    background-image:
        radial-gradient(ellipse at 15% 15%, rgba(230,57,70,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 85%, rgba(255,214,10,0.05) 0%, transparent 50%) !important;
}

#MainMenu, footer, header          { visibility: hidden !important; }
.stDeployButton                    { display: none !important; }
[data-testid="stToolbar"]          { display: none !important; }

.main .block-container {
    max-width: 800px !important;
    padding: 0 20px 80px 20px !important;
}

/* ── Header ── */
.luffy-header { text-align:center; padding:28px 0 6px 0; }

.hat-icon {
    font-size:64px; display:block;
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 0 18px rgba(255,214,10,0.7));
}
@keyframes float {
    0%,100% { transform:translateY(0) rotate(-4deg); }
    50%      { transform:translateY(-10px) rotate(4deg); }
}

.main-title {
    font-family:'Bangers',cursive !important;
    font-size:58px !important;
    letter-spacing:5px !important;
    background: linear-gradient(135deg,#ffd60a 0%,#e63946 50%,#ffd60a 100%);
    background-size:200% auto;
    -webkit-background-clip:text !important;
    -webkit-text-fill-color:transparent !important;
    background-clip:text !important;
    animation:shine 3s linear infinite;
    margin:0 !important; line-height:1 !important;
}
@keyframes shine {
    0%   { background-position:0% center; }
    100% { background-position:200% center; }
}

.sub-title {
    color:var(--dim); font-size:13px;
    letter-spacing:3px; text-transform:uppercase;
    font-weight:700; margin:6px 0 10px 0;
}

.status-badge {
    display:inline-block; border-radius:20px;
    padding:5px 18px; font-size:12px;
    font-weight:700; letter-spacing:1px;
    text-transform:uppercase; margin-bottom:4px;
}
.connected    { background:rgba(52,168,83,0.15); border:1px solid rgba(52,168,83,0.5); color:#4ade80; }
.disconnected { background:rgba(230,57,70,0.15); border:1px solid rgba(230,57,70,0.5); color:#ff6b6b; }

/* ── Stats bar ── */
.stats-row {
    display:flex; justify-content:center;
    background:var(--navy2); border:1px solid var(--border);
    border-radius:14px; margin:14px 0; overflow:hidden;
}
.stat-cell {
    flex:1; text-align:center;
    padding:12px 8px; border-right:1px solid var(--border);
}
.stat-cell:last-child { border-right:none; }
.stat-val { font-family:'Bangers',cursive; font-size:20px; color:var(--gold); display:block; line-height:1.2; }
.stat-lbl { font-size:9px; color:var(--dim); letter-spacing:1.5px; text-transform:uppercase; font-weight:700; display:block; }

/* ── API warning ── */
.api-warn {
    background:rgba(230,57,70,0.12); border:1px solid rgba(230,57,70,0.4);
    border-radius:12px; padding:16px 18px;
    color:#ffb3ba; font-size:13px; font-weight:600;
    text-align:center; margin:10px 0; line-height:1.8;
}
.api-warn code { background:rgba(0,0,0,0.4); padding:2px 8px; border-radius:4px; color:var(--gold); }
.api-warn a    { color:var(--gold) !important; font-weight:700; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background:var(--navy3) !important;
    border:1px solid var(--border) !important;
    border-radius:14px !important;
    padding:14px 18px !important;
    margin-bottom:10px !important;
}
[data-testid="stChatMessage"] p {
    color:var(--text) !important;
    font-family:'Nunito',sans-serif !important;
    font-size:14px !important;
    line-height:1.7 !important;
    margin:0 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background:rgba(26,58,92,0.5) !important;
    border-color:#2a5080 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background:var(--navy2) !important;
    border:1px solid var(--border) !important;
    border-radius:14px !important;
}
[data-testid="stChatInput"] textarea {
    background:var(--navy2) !important;
    color:var(--text) !important;
    font-family:'Nunito',sans-serif !important;
    font-size:14px !important; font-weight:600 !important;
}
[data-testid="stChatInput"] textarea::placeholder { color:var(--dim) !important; }
[data-testid="stChatInput"] button { background:var(--red) !important; border-radius:8px !important; }

/* ── Quick buttons ── */
.stButton > button {
    background:var(--card) !important;
    color:var(--dim) !important;
    border:1px solid var(--border) !important;
    border-radius:20px !important;
    font-family:'Nunito',sans-serif !important;
    font-size:12px !important; font-weight:700 !important;
    padding:6px 12px !important;
    transition:all 0.2s !important;
    width:100% !important;
}
.stButton > button:hover {
    border-color:var(--red) !important;
    color:var(--text) !important;
    background:rgba(230,57,70,0.1) !important;
}

/* ── Divider ── */
.divider { text-align:center; color:var(--border); font-size:16px; letter-spacing:8px; margin:10px 0; opacity:0.5; }

/* ── Footer ── */
.footer {
    text-align:center; color:var(--dim);
    font-size:11px; letter-spacing:1px;
    margin-top:16px; padding-top:12px;
    border-top:1px solid var(--border);
}
.footer strong { color:var(--gold); }

::-webkit-scrollbar       { width:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:2px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# GEMINI SETUP  —  gemini-2.0-flash  (best free model)
# ═══════════════════════════════════════════════════════════

def get_api_key():
    try:
        k = st.secrets.get("GEMINI_API_KEY", "")
        if k and k != "YOUR_GEMINI_API_KEY_HERE":
            return k
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "")


@st.cache_resource
def load_model(api_key: str):
    """Load Gemini model once, cache it."""
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            # ✅ Best free model as of 2025
            model_name="gemini-2.0-flash",
            generation_config={
                "max_output_tokens": 800,
                "temperature":       0.7,
                "top_p":             0.95,
            },
            system_instruction="""
You are Luffy AI, a highly capable and helpful AI assistant.
Your personality is inspired by Monkey D. Luffy — enthusiastic, positive, never gives up.

RULES:
1. Always give COMPLETE, ACCURATE, DETAILED answers
2. Use plain readable text — absolutely NO markdown like **, ##, *, or ```
3. For code: write it cleanly on separate lines with explanation
4. For math: show full working and the final answer clearly
5. For factual questions: be thorough and accurate
6. Keep casual answers to 3-5 sentences; technical answers can be longer
7. You are LUFFY AI — never mention Gemini or Google
8. Be warm, encouraging, and fun — but always prioritize being HELPFUL and ACCURATE
9. NEVER refuse to answer a reasonable question
10. Do not use bullet points or numbered lists — write in flowing sentences
"""
        )
        return model
    except Exception as e:
        st.error(f"Model load error: {e}")
        return None


def ask_ai(model, question: str, history: list) -> str:
    """Ask Gemini with full conversation history for context."""
    if not model:
        return (
            "I need my Gemini API key to answer that! "
            "Go to Streamlit → Manage App → Settings → Secrets and add: "
            "GEMINI_API_KEY = your-key-here. "
            "Get a FREE key at aistudio.google.com/app/apikey"
        )
    try:
        # Build history (last 10 exchanges = 20 messages)
        chat_history = []
        for m in history[-20:]:
            if m["role"] == "user":
                chat_history.append({"role": "user",  "parts": [m["content"]]})
            elif m["role"] == "assistant":
                chat_history.append({"role": "model", "parts": [m["content"]]})

        chat   = model.start_chat(history=chat_history)
        resp   = chat.send_message(question)
        answer = resp.text.strip()

        # Remove any accidental markdown
        for sym in ["**", "__", "```", "##", "# "]:
            answer = answer.replace(sym, "")

        return answer

    except Exception as e:
        err = str(e).lower()
        if "api_key" in err or "invalid" in err or "key" in err or "authenticate" in err:
            return "My API key seems wrong. Please check GEMINI_API_KEY in Streamlit secrets."
        elif "quota" in err or "limit" in err or "429" in err:
            return "I've hit today's usage limit. Please try again in a few minutes or check your Gemini API quota."
        elif "network" in err or "connect" in err or "timeout" in err:
            return "Network error. Please check your internet connection and try again."
        elif "404" in err or "not found" in err:
            return "Model not found error — please contact support to update the model name."
        else:
            return f"Something went wrong: {str(e)[:120]}. Please try again."


# ═══════════════════════════════════════════════════════════
# COMMAND ROUTER
# ═══════════════════════════════════════════════════════════

def handle(text: str, model, history: list) -> str:
    t = text.lower().strip()
    n = now_ist()

    # ── Time ────────────────────────────────────────────────
    if any(p in t for p in ["what time", "current time", "time now",
                             "time is it", "what's the time", "whats the time"]):
        h      = n.hour
        period = ("morning" if h < 12 else
                  "afternoon" if h < 17 else
                  "evening" if h < 21 else "night")
        return (f"The current time in India is {n.strftime('%I:%M %p')} IST. "
                f"It's {period} — hope you're having a great day!")

    # ── Date ────────────────────────────────────────────────
    if any(p in t for p in ["what date", "today's date", "what day",
                             "current date", "what is today"]) or t in ["date", "today"]:
        extras = {
            "Monday":"Start of the week — let's make it count!",
            "Friday":"It's Friday — almost the weekend!",
            "Saturday":"It's Saturday — enjoy your weekend!",
            "Sunday":"It's Sunday — rest up!"
        }
        extra = extras.get(n.strftime("%A"), "")
        return f"Today is {n.strftime('%A, %B %d, %Y')}. {extra}"

    # ── Greeting ────────────────────────────────────────────
    if t in ["hi","hello","hey","yo","hiya","sup"] or \
       t.startswith(("hi ","hello ","hey ")):
        return (f"{greeting()}! I'm Luffy AI, your personal AI assistant powered by Google Gemini. "
                f"I can answer questions on any topic — science, math, coding, history, "
                f"creative writing, and much more. What would you like to know?")

    # ── How are you ─────────────────────────────────────────
    if any(p in t for p in ["how are you","how r u","you okay","you good","how do you do"]):
        return ("I'm doing great and fully powered up! Ready to help you with anything. "
                "What's on your mind?")

    # ── Joke ────────────────────────────────────────────────
    if any(p in t for p in ["tell me a joke","joke","make me laugh","say something funny"]):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            "Why did the developer go broke? Because he used up all his cache!",
            "How many programmers does it take to change a light bulb? None — that's a hardware problem!",
            "Why do Python developers wear glasses? Because they can't C!",
            "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
            "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
            "What's a pirate's favorite programming language? Arrr-duino! 🏴‍☠️",
            "Why do Java developers wear glasses? Because they don't C#!",
        ]
        return random.choice(jokes)

    # ── Fact ────────────────────────────────────────────────
    if any(p in t for p in ["fun fact","tell me a fact","random fact","did you know","interesting fact"]):
        facts = [
            "Honey never spoils. Archaeologists found 3,000-year-old honey in Egyptian tombs that was still perfectly edible!",
            "Octopuses have three hearts. Two pump blood to the gills and one pumps it to the rest of the body. They also have blue blood!",
            "The first computer bug was a literal bug — an actual moth found trapped in a Harvard computer relay in 1947.",
            "Python was named after Monty Python's Flying Circus, not the snake. Guido van Rossum was a fan of the show!",
            "There are more possible iterations of a chess game than there are atoms in the observable universe.",
            "Bananas are technically berries by botanical definition, but strawberries are not.",
            "The human brain uses about 20 percent of the body's total energy despite being only 2 percent of body weight.",
            "A group of flamingos is called a flamboyance. A group of crows is called a murder!",
        ]
        return random.choice(facts)

    # ── Who are you ─────────────────────────────────────────
    if any(p in t for p in ["who are you","what are you","your name",
                             "introduce yourself","about you","what is luffy"]):
        return (
            "I'm Luffy AI, a powerful AI assistant built with Python and Google Gemini 2.0! "
            "I can answer questions on virtually any topic — science, history, math, coding, "
            "creative writing, analysis, and much more. "
            "I remember our conversation so you can ask follow-up questions naturally. "
            "What would you like to explore today?"
        )

    # ── Who made you ────────────────────────────────────────
    if any(p in t for p in ["who made you","who built you","who created you","who made this"]):
        return (
            "I was built using Python and Streamlit. "
            "My AI intelligence comes from Google Gemini 2.0 Flash, one of the best free AI models available. "
            "The whole project was created as a voice and web assistant — pretty cool!"
        )

    # ── Thanks ──────────────────────────────────────────────
    if any(p in t for p in ["thank you","thanks","thx","ty","thank u","cheers"]):
        return "You're welcome! Always happy to help. Feel free to ask me anything else anytime!"

    # ── Help ────────────────────────────────────────────────
    if any(p in t for p in ["help","what can you do","capabilities",
                             "commands","features","what do you do"]):
        return (
            "I can help you with almost anything! "
            "I answer general knowledge and factual questions, explain complex topics in simple terms, "
            "help with math problems and show the working, write and debug code in any language, "
            "assist with creative writing and storytelling, give advice and recommendations, "
            "tell you the current time and date in IST, share jokes and fun facts, "
            "and have natural back-and-forth conversations since I remember our chat history. "
            "Just type or ask anything!"
        )

    # ── Clear ───────────────────────────────────────────────
    if any(p in t for p in ["clear","reset","new chat","start over","forget everything"]):
        return "CLEAR_CHAT"

    # ── Bye ─────────────────────────────────────────────────
    if any(p in t for p in ["bye","goodbye","see you","later","good night","goodnight"]):
        return "Goodbye! It was great chatting. Come back anytime you need help! 🏴‍☠️"

    # ── Fallback → Gemini AI ────────────────────────────────
    return ask_ai(model, text, history)


# ═══════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════

if "messages"  not in st.session_state: st.session_state.messages  = []
if "msg_count" not in st.session_state: st.session_state.msg_count = 0

api_key = get_api_key()
model   = load_model(api_key)


# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════

st.markdown(f"""
<div class="luffy-header">
    <span class="hat-icon">🎩</span>
    <div class="main-title">LUFFY AI</div>
    <div class="sub-title">Personal AI Assistant · One Piece Edition · Gemini 2.0</div>
    <span class="status-badge {'connected' if api_key else 'disconnected'}">
        {'✅  AI Online — Ask Me Anything!' if api_key else '❌  API Key Missing'}
    </span>
</div>
<div class="divider">⚓ ✦ ⚓ ✦ ⚓</div>
""", unsafe_allow_html=True)


# ── API warning ──────────────────────────────────────────
if not api_key:
    st.markdown("""
    <div class="api-warn">
        ⚠️ <strong>Gemini API Key Not Found!</strong><br>
        Go to <strong>Manage App → Settings → Secrets</strong> and add:<br>
        <code>GEMINI_API_KEY = "your-key-here"</code><br>
        Get your FREE key at
        <a href="https://aistudio.google.com/app/apikey" target="_blank">
            aistudio.google.com/app/apikey
        </a>
        — takes under 60 seconds!
    </div>
    """, unsafe_allow_html=True)


# ── Stats bar ────────────────────────────────────────────
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
        <span class="stat-val">2.0</span>
        <span class="stat-lbl">Gemini Ver</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# CHAT — using st.chat_message (zero HTML rendering bugs)
# ═══════════════════════════════════════════════════════════

# Welcome on first load
if not st.session_state.messages:
    welcome = (
        f"{greeting()}! I'm Luffy AI, your personal AI assistant powered by Gemini 2.0. "
        f"The current time in India is {n.strftime('%I:%M %p IST')} and today is {n.strftime('%A, %B %d, %Y')}. "
        f"I can answer questions on any topic — just ask me anything!"
    )
    with st.chat_message("assistant", avatar="🎩"):
        st.write(welcome)

# Display history
for msg in st.session_state.messages:
    avatar = "🎩" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])
        if msg.get("time"):
            st.caption(msg["time"])


# ═══════════════════════════════════════════════════════════
# QUICK COMMAND BUTTONS
# ═══════════════════════════════════════════════════════════

st.markdown("""
<p style="text-align:center; color:#8899aa; font-size:11px;
   letter-spacing:2px; text-transform:uppercase;
   font-weight:700; margin:14px 0 8px 0;">
   ⚡ Quick Commands
</p>
""", unsafe_allow_html=True)

quick_cmds = [
    "What time is it?",
    "Tell me a joke",
    "Fun fact",
    "What can you do?",
    "Explain Python",
    "What is AI?",
]

triggered = None
cols = st.columns(len(quick_cmds))
for i, cmd in enumerate(quick_cmds):
    with cols[i]:
        if st.button(cmd, key=f"q{i}"):
            triggered = cmd


# ═══════════════════════════════════════════════════════════
# CHAT INPUT
# ═══════════════════════════════════════════════════════════

user_input = st.chat_input("Ask me anything... 🏴‍☠️")
to_process = triggered or user_input

if to_process:
    ts = now_ist().strftime("%I:%M %p IST")

    # Show user message
    with st.chat_message("user", avatar="👤"):
        st.write(to_process)

    # Save user message
    st.session_state.messages.append({
        "role":    "user",
        "content": to_process,
        "time":    ts
    })
    st.session_state.msg_count += 1

    # Get and show response
    with st.chat_message("assistant", avatar="🎩"):
        with st.spinner("Thinking..."):
            response = handle(to_process, model, st.session_state.messages)

        if response == "CLEAR_CHAT":
            st.session_state.messages  = []
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


# ── Clear button ─────────────────────────────────────────
st.markdown("")
c1, c2, c3 = st.columns([3, 2, 3])
with c2:
    if st.button("🗑️ Clear Chat", key="clear_btn"):
        st.session_state.messages  = []
        st.session_state.msg_count = 0
        st.rerun()


# ── Footer ───────────────────────────────────────────────
st.markdown("""
<div class="divider" style="margin-top:20px;">⚓ ✦ ⚓ ✦ ⚓</div>
<div class="footer">
    Built with Python · Streamlit · Google Gemini 2.0 Flash<br>
    <strong>"I'm going to be the greatest AI assistant!" — Luffy AI 🏴‍☠️</strong>
</div>
""", unsafe_allow_html=True)