# ============================================
# app.py — Nova Web Version
# Deployed on Streamlit Cloud
# Text-based interface (no mic needed online)
# ============================================

import streamlit as st
import os

# ---- Page Config ----
st.set_page_config(
    page_title="Nova — AI Voice Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---- Custom CSS (Gemini Dark Theme) ----
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');

    /* Main background */
    .stApp {
        background-color: #131314;
        font-family: 'Google Sans', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Chat message styling */
    .user-bubble {
        background: #1e3a5f;
        color: #c2e7ff;
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 75%;
        float: right;
        clear: both;
        font-size: 15px;
        line-height: 1.5;
    }

    .nova-bubble {
        background: #1e1f20;
        color: #e3e3e3;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 75%;
        float: left;
        clear: both;
        font-size: 15px;
        line-height: 1.5;
        border: 1px solid #3c4043;
    }

    .nova-name {
        color: #8ab4f8;
        font-weight: 700;
        font-size: 13px;
        margin-bottom: 4px;
    }

    .user-name {
        color: #4285f4;
        font-weight: 700;
        font-size: 13px;
        margin-bottom: 4px;
        text-align: right;
    }

    /* Input styling */
    .stTextInput input {
        background-color: #282a2c !important;
        color: #e3e3e3 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 24px !important;
        padding: 12px 20px !important;
        font-size: 15px !important;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #4285f4, #1a73e8) !important;
        color: white !important;
        border: none !important;
        border-radius: 24px !important;
        padding: 10px 28px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
    }

    /* Title styling */
    h1 {
        color: #e3e3e3 !important;
        font-weight: 700 !important;
    }

    p {
        color: #9aa0a6 !important;
    }

    /* Clear float */
    .clearfix::after {
        content: "";
        display: table;
        clear: both;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# GEMINI SETUP
# ============================================

@st.cache_resource
def setup_gemini():
    """
    Sets up Gemini AI.
    Uses Streamlit secrets for API key
    (safe — never exposed publicly)
    """
    try:
        import google.generativeai as genai

        # Get API key from Streamlit secrets
        # We'll set this up on Streamlit Cloud
        api_key = st.secrets.get("GEMINI_API_KEY", "")

        if not api_key:
            return None

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "max_output_tokens": 300,
                "temperature": 0.7,
            },
            system_instruction="""
            You are Nova, a helpful personal AI voice assistant.
            Keep ALL responses under 3 sentences maximum.
            Never use bullet points, markdown, or special symbols.
            Speak naturally and conversationally.
            Be warm, helpful and slightly witty.
            """
        )
        return model

    except Exception as e:
        return None


# ============================================
# COMMAND HANDLER (Web Version)
# ============================================

def handle_web_command(text, model):
    """
    Handles commands for web version.
    No mic/speaker — text only.
    """
    import datetime
    import webbrowser

    text_lower = text.lower().strip()

    # ---- Time ----
    if "time" in text_lower:
        now = datetime.datetime.now()
        return f"It is {now.strftime('%I:%M %p')} right now."

    # ---- Date ----
    elif "date" in text_lower or "today" in text_lower:
        now = datetime.datetime.now()
        return f"Today is {now.strftime('%A, %B %d %Y')}."

    # ---- Greeting ----
    elif any(w in text_lower for w in ["hello", "hi", "hey"]):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            g = "Good morning"
        elif 12 <= hour < 17:
            g = "Good afternoon"
        else:
            g = "Good evening"
        return f"{g}! I'm Nova, your AI assistant. How can I help you today?"

    # ---- How are you ----
    elif "how are you" in text_lower:
        return "I'm doing great, thank you for asking! How can I assist you today?"

    # ---- Joke ----
    elif "joke" in text_lower:
        import random
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the programmer quit? Because he didn't get arrays!",
            "Why do Python programmers wear glasses? Because they can't C!",
        ]
        return random.choice(jokes)

    # ---- Help ----
    elif "help" in text_lower or "what can you do" in text_lower:
        return ("I can answer any question using Gemini AI, tell you the time and date, "
                "crack jokes, share fun facts, and have a full conversation with you!")

    # ---- AI fallback ----
    else:
        if model:
            try:
                response = model.generate_content(text)
                answer = response.text.strip()
                # Clean markdown
                for char in ["*", "#", "`", "**", "__"]:
                    answer = answer.replace(char, "")
                return answer
            except Exception as e:
                return "I had trouble thinking of a response. Please try again!"
        else:
            return ("I need a Gemini API key to answer that. "
                    "Add GEMINI_API_KEY to Streamlit secrets to enable AI responses!")


# ============================================
# STREAMLIT UI
# ============================================

def main():

    # ---- Header ----
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 30px 0 10px 0;'>
            <div style='font-size:48px'>🤖</div>
            <h1 style='font-size:36px; margin:8px 0 4px 0;'>Nova</h1>
            <p style='font-size:15px; color:#9aa0a6;'>
                Personal AI Voice Assistant
            </p>
            <div style='display:inline-block; background:#1e1f20;
                        border:1px solid #34a853; border-radius:20px;
                        padding:4px 16px; margin-top:8px;'>
                <span style='color:#34a853; font-size:12px;
                             font-weight:600;'>● Online</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ---- Setup Gemini ----
    model = setup_gemini()

    # ---- Initialize chat history ----
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "nova",
            "content": "Hello! I'm Nova, your personal AI assistant. Ask me anything!"
        })

    # ---- Display chat history ----
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "nova":
                st.markdown(f"""
                <div class='clearfix'>
                    <div class='nova-name'>🤖 Nova</div>
                    <div class='nova-bubble'>{msg['content']}</div>
                </div>
                <br>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='clearfix'>
                    <div class='user-name'>You 👤</div>
                    <div class='user-bubble'>{msg['content']}</div>
                </div>
                <br>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---- Input area ----
    col1, col2 = st.columns([5, 1])

    with col1:
        user_input = st.text_input(
            label="message",
            placeholder="Ask Nova anything...",
            label_visibility="collapsed",
            key="user_input"
        )

    with col2:
        send = st.button("Send ➤", use_container_width=True)

    # ---- Handle send ----
    if send and user_input.strip():
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input.strip()
        })

        # Get Nova's response
        with st.spinner("Nova is thinking..."):
            response = handle_web_command(user_input.strip(), model)

        # Add Nova's response
        st.session_state.messages.append({
            "role": "nova",
            "content": response
        })

        # Rerun to show new messages
        st.rerun()

    # ---- Clear chat ----
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = [{
            "role": "nova",
            "content": "Chat cleared! How can I help you?"
        }]
        st.rerun()

    # ---- Footer ----
    st.markdown("""
    <div style='text-align:center; padding:20px 0; color:#5f6368; font-size:12px;'>
        Built with Python + Streamlit + Gemini AI
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()