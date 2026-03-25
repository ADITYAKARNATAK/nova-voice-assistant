# ============================================================
#
#   ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗
#   ████╗  ██║██╔═══██╗██║   ██║██╔══██╗
#   ██╔██╗ ██║██║   ██║██║   ██║███████║
#   ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
#   ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
#   ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝
#
#   Nova — Personal AI Voice Assistant
#   Gemini-Style GUI — Final Version
#   Built with Python + Tkinter
#
# ============================================================

# ---- Standard Library ----
import tkinter as tk
from tkinter import scrolledtext, font
import threading        # Run mic listening in background
import time
import queue            # Thread-safe message passing
import math             # For mic animation pulse
import datetime

# ---- Third Party ----
import speech_recognition as sr
import pyttsx3

# ---- Our Modules ----
from utils import (
    tell_time, tell_date, greet_user,
    tell_joke, tell_weather, tell_fact,
    system_status, get_greeting
)
from websites import open_website, open_app, handle_search


# ============================================================
# CONFIGURATION
# ============================================================

ASSISTANT_NAME = "Nova"
LANGUAGE       = "en-in"        # Change to "en-us" if needed
SPEECH_RATE    = 150
SPEECH_VOLUME  = 1.0
LISTEN_TIMEOUT = 6
MAX_RETRIES    = 3

# ---- Gemini-Inspired Dark Color Palette ----
COLORS = {
    # Backgrounds
    "bg_deep"       : "#0d0d0d",   # Deepest background
    "bg_main"       : "#131314",   # Main window background
    "bg_sidebar"    : "#1a1a1b",   # Sidebar / panel
    "bg_card"       : "#1e1f20",   # Card / bubble background
    "bg_input"      : "#282a2c",   # Input field background
    "bg_hover"      : "#2d2f31",   # Hover state

    # User bubble
    "bubble_user"   : "#1e3a5f",   # User message bubble
    "bubble_nova"   : "#1e1f20",   # Nova message bubble

    # Text
    "text_primary"  : "#e3e3e3",   # Main text
    "text_secondary": "#9aa0a6",   # Dim text
    "text_user"     : "#c2e7ff",   # User message text

    # Accents — Gemini blue-teal gradient feel
    "accent_blue"   : "#4285f4",   # Google blue
    "accent_teal"   : "#1a73e8",   # Teal accent
    "accent_glow"   : "#8ab4f8",   # Glow / highlight
    "accent_green"  : "#34a853",   # Success green
    "accent_red"    : "#ea4335",   # Error red
    "accent_yellow" : "#fbbc05",   # Warning yellow

    # Mic button states
    "mic_idle"      : "#4285f4",   # Normal blue
    "mic_listening" : "#ea4335",   # Red when listening
    "mic_processing": "#fbbc05",   # Yellow when processing

    # Borders
    "border"        : "#3c4043",   # Subtle border
    "border_focus"  : "#4285f4",   # Focused border
}

# ---- Fonts ----
FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_SUB    = ("Segoe UI", 11)
FONT_CHAT   = ("Segoe UI", 12)
FONT_INPUT  = ("Segoe UI", 13)
FONT_SMALL  = ("Segoe UI", 9)
FONT_STATUS = ("Segoe UI", 10)
FONT_MIC    = ("Segoe UI", 18)


# ============================================================
# SPEECH ENGINE
# ============================================================

def create_tts_engine():
    """Creates and configures the pyttsx3 TTS engine."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    try:
        engine.setProperty('voice', voices[1].id)
    except IndexError:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', SPEECH_RATE)
    engine.setProperty('volume', SPEECH_VOLUME)
    return engine


# ============================================================
# NOVA GUI APPLICATION CLASS
# ============================================================

class NovaApp:
    """
    Main Nova Voice Assistant GUI Application.
    Gemini-style dark interface with:
    - Animated mic button
    - Chat bubble interface
    - Live status indicators
    - Text + voice input
    - Threaded listening (non-blocking UI)
    """

    def __init__(self, root):
        self.root = root
        self.root.title(f"{ASSISTANT_NAME} — AI Voice Assistant")
        self.root.geometry("900x700")
        self.root.minsize(700, 550)
        self.root.configure(bg=COLORS["bg_main"])

        # ---- State Variables ----
        self.is_listening   = False     # True when mic is active
        self.is_speaking    = False     # True when Nova is speaking
        self.is_processing  = False     # True when processing speech
        self.mic_anim_id    = None      # Animation loop ID
        self.pulse_angle    = 0         # Mic pulse animation angle
        self.message_count  = 0         # Total messages sent
        self.running        = True      # App running state

        # ---- Thread Communication Queue ----
        # Threads put messages here → UI reads safely
        self.msg_queue = queue.Queue()

        # ---- Build the UI ----
        self._build_ui()

        # ---- Start queue processor ----
        self._process_queue()

        # ---- Welcome Message ----
        greeting = get_greeting()
        welcome = (f"{greeting}! I'm {ASSISTANT_NAME}, your personal AI assistant.\n"
                   f"Click the mic button or type below to get started!")
        self.root.after(500, lambda: self._add_nova_message(welcome))

        # ---- Handle window close ----
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)


    # ========================================================
    # UI BUILDER
    # ========================================================

    def _build_ui(self):
        """Builds the complete Gemini-style interface."""

        # ---- ROOT GRID ----
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # ---- OUTER FRAME ----
        outer = tk.Frame(self.root, bg=COLORS["bg_main"])
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_rowconfigure(1, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        # Build sections
        self._build_header(outer)
        self._build_chat_area(outer)
        self._build_status_bar(outer)
        self._build_input_area(outer)


    def _build_header(self, parent):
        """Top header bar — Nova branding + controls."""

        header = tk.Frame(parent, bg=COLORS["bg_sidebar"],
                          height=64, pady=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)

        # ---- Left: Logo + Name ----
        logo_frame = tk.Frame(header, bg=COLORS["bg_sidebar"])
        logo_frame.grid(row=0, column=0, padx=20, pady=12, sticky="w")

        # Animated logo canvas (small gem shape)
        self.logo_canvas = tk.Canvas(
            logo_frame, width=38, height=38,
            bg=COLORS["bg_sidebar"], highlightthickness=0
        )
        self.logo_canvas.pack(side="left", padx=(0, 10))
        self._draw_gem_logo()

        # Name label
        name_frame = tk.Frame(logo_frame, bg=COLORS["bg_sidebar"])
        name_frame.pack(side="left")

        tk.Label(
            name_frame, text=ASSISTANT_NAME,
            font=("Segoe UI", 18, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg_sidebar"]
        ).pack(anchor="w")

        tk.Label(
            name_frame, text="Personal AI Voice Assistant",
            font=FONT_SMALL,
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_sidebar"]
        ).pack(anchor="w")

        # ---- Center: Status pill ----
        center_frame = tk.Frame(header, bg=COLORS["bg_sidebar"])
        center_frame.grid(row=0, column=1, pady=12)

        self.status_pill = tk.Label(
            center_frame,
            text="● Ready",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS["accent_green"],
            bg=COLORS["bg_card"],
            padx=14, pady=5,
            relief="flat",
            bd=0
        )
        self.status_pill.pack()

        # ---- Right: Clear button ----
        right_frame = tk.Frame(header, bg=COLORS["bg_sidebar"])
        right_frame.grid(row=0, column=2, padx=20, pady=12, sticky="e")

        clear_btn = tk.Button(
            right_frame,
            text="⊘  Clear Chat",
            font=FONT_SMALL,
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_hover"],
            activeforeground=COLORS["text_primary"],
            activebackground=COLORS["border"],
            relief="flat", bd=0, padx=12, pady=6,
            cursor="hand2",
            command=self._clear_chat
        )
        clear_btn.pack()

        # Separator line
        sep = tk.Frame(parent, bg=COLORS["border"], height=1)
        sep.grid(row=0, column=0, sticky="sew")


    def _draw_gem_logo(self):
        """Draws an animated gem/diamond logo on canvas."""
        c = self.logo_canvas
        c.delete("all")

        # Draw gradient-like gem shape using polygons
        # Outer gem
        pts_outer = [19, 2, 36, 14, 36, 26, 19, 36, 2, 26, 2, 14]
        c.create_polygon(pts_outer, fill=COLORS["accent_blue"],
                         outline=COLORS["accent_glow"], width=1)

        # Inner highlight
        pts_inner = [19, 8, 30, 16, 19, 28, 8, 16]
        c.create_polygon(pts_inner, fill=COLORS["accent_teal"],
                         outline="", width=0)

        # Center dot
        c.create_oval(15, 15, 23, 23, fill=COLORS["accent_glow"],
                      outline="")


    def _build_chat_area(self, parent):
        """Main chat display area with scrolling bubbles."""

        # Chat container with subtle inner border
        chat_outer = tk.Frame(parent, bg=COLORS["border"], padx=1, pady=0)
        chat_outer.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        chat_outer.grid_rowconfigure(0, weight=1)
        chat_outer.grid_columnconfigure(0, weight=1)

        # Scrollable canvas for chat bubbles
        self.chat_canvas = tk.Canvas(
            chat_outer,
            bg=COLORS["bg_main"],
            highlightthickness=0,
            bd=0
        )
        self.chat_canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbar (hidden unless hovered — Gemini style)
        self.scrollbar = tk.Scrollbar(
            chat_outer,
            orient="vertical",
            command=self.chat_canvas.yview,
            bg=COLORS["bg_main"],
            troughcolor=COLORS["bg_main"],
            width=6
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Inner frame that holds all message widgets
        self.chat_frame = tk.Frame(self.chat_canvas, bg=COLORS["bg_main"])
        self.chat_window = self.chat_canvas.create_window(
            (0, 0), window=self.chat_frame, anchor="nw"
        )

        # Bind resize
        self.chat_frame.bind("<Configure>", self._on_chat_resize)
        self.chat_canvas.bind("<Configure>", self._on_canvas_resize)

        # Mouse wheel scrolling
        self.chat_canvas.bind_all("<MouseWheel>", self._on_mousewheel)


    def _build_status_bar(self, parent):
        """Live status bar below chat, above input."""

        status_frame = tk.Frame(parent, bg=COLORS["bg_sidebar"],
                                height=32, pady=0)
        status_frame.grid(row=2, column=0, sticky="ew")
        status_frame.grid_propagate(False)
        status_frame.grid_columnconfigure(1, weight=1)

        # Left: waveform animation canvas
        self.wave_canvas = tk.Canvas(
            status_frame, width=80, height=32,
            bg=COLORS["bg_sidebar"], highlightthickness=0
        )
        self.wave_canvas.grid(row=0, column=0, padx=(16, 8))
        self._draw_idle_wave()

        # Center: status text
        self.status_label = tk.Label(
            status_frame,
            text="Ready — say something or type below",
            font=FONT_STATUS,
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_sidebar"],
            anchor="w"
        )
        self.status_label.grid(row=0, column=1, sticky="w")

        # Right: message count
        self.count_label = tk.Label(
            status_frame,
            text="0 messages",
            font=FONT_SMALL,
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_sidebar"]
        )
        self.count_label.grid(row=0, column=2, padx=16)


    def _build_input_area(self, parent):
        """Bottom input bar — text field + mic button + send."""

        input_bg = tk.Frame(parent, bg=COLORS["bg_sidebar"], pady=16)
        input_bg.grid(row=3, column=0, sticky="ew")
        input_bg.grid_columnconfigure(0, weight=1)

        # Inner container
        inner = tk.Frame(input_bg, bg=COLORS["bg_sidebar"])
        inner.grid(row=0, column=0, padx=20, sticky="ew")
        inner.grid_columnconfigure(0, weight=1)

        # ---- Input pill (text field) ----
        pill_frame = tk.Frame(
            inner,
            bg=COLORS["bg_input"],
            pady=2, padx=4,
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        pill_frame.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        pill_frame.grid_columnconfigure(0, weight=1)

        self.text_input = tk.Text(
            pill_frame,
            font=FONT_INPUT,
            fg=COLORS["text_primary"],
            bg=COLORS["bg_input"],
            insertbackground=COLORS["accent_glow"],
            relief="flat",
            bd=0,
            height=2,
            wrap="word",
            padx=14, pady=10
        )
        self.text_input.grid(row=0, column=0, sticky="ew")
        self.text_input.insert("1.0", "Type a message or click the mic...")
        self.text_input.configure(fg=COLORS["text_secondary"])

        # Placeholder behavior
        self.text_input.bind("<FocusIn>",  self._on_input_focus)
        self.text_input.bind("<FocusOut>", self._on_input_blur)
        self.text_input.bind("<Return>",   self._on_enter_key)

        # Send icon button inside pill
        send_btn = tk.Button(
            pill_frame,
            text="➤",
            font=("Segoe UI", 14),
            fg=COLORS["accent_blue"],
            bg=COLORS["bg_input"],
            activeforeground=COLORS["accent_glow"],
            activebackground=COLORS["bg_input"],
            relief="flat", bd=0,
            padx=10, pady=6,
            cursor="hand2",
            command=self._send_text
        )
        send_btn.grid(row=0, column=1, padx=(0, 4))

        # ---- Mic Button ----
        self.mic_frame = tk.Frame(inner, bg=COLORS["bg_sidebar"])
        self.mic_frame.grid(row=0, column=1)

        # Outer glow ring canvas
        self.mic_canvas = tk.Canvas(
            self.mic_frame, width=64, height=64,
            bg=COLORS["bg_sidebar"], highlightthickness=0
        )
        self.mic_canvas.pack()
        self.mic_canvas.bind("<Button-1>", self._on_mic_click)
        self.mic_canvas.bind("<Enter>",    self._on_mic_hover)
        self.mic_canvas.bind("<Leave>",    self._on_mic_leave)

        # Draw initial mic button state
        self._draw_mic_button("idle")

        # Hint text
        tk.Label(
            input_bg,
            text="Press Enter to send  •  Click mic for voice  •  Say 'exit' to quit",
            font=FONT_SMALL,
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_sidebar"]
        ).grid(row=1, column=0, pady=(6, 0))


    # ========================================================
    # MIC BUTTON DRAWING & ANIMATION
    # ========================================================

    def _draw_mic_button(self, state="idle"):
        """
        Draws the circular mic button.
        States: idle, listening, processing, speaking
        """
        c = self.mic_canvas
        c.delete("all")

        # Choose colors based on state
        if state == "idle":
            ring_color  = COLORS["bg_card"]
            btn_color   = COLORS["mic_idle"]
            icon_color  = "#ffffff"
            ring_width  = 2
        elif state == "listening":
            ring_color  = COLORS["mic_listening"]
            btn_color   = COLORS["mic_listening"]
            icon_color  = "#ffffff"
            ring_width  = 3
        elif state == "processing":
            ring_color  = COLORS["mic_processing"]
            btn_color   = COLORS["bg_card"]
            icon_color  = COLORS["mic_processing"]
            ring_width  = 3
        elif state == "speaking":
            ring_color  = COLORS["accent_green"]
            btn_color   = COLORS["bg_card"]
            icon_color  = COLORS["accent_green"]
            ring_width  = 2
        else:
            ring_color  = COLORS["border"]
            btn_color   = COLORS["bg_card"]
            icon_color  = COLORS["text_secondary"]
            ring_width  = 1

        # Outer ring
        c.create_oval(2, 2, 62, 62,
                      outline=ring_color,
                      width=ring_width,
                      fill="")

        # Main circle button
        c.create_oval(8, 8, 56, 56,
                      fill=btn_color,
                      outline="")

        # Microphone icon (drawn with shapes)
        # Mic body
        c.create_rectangle(26, 18, 38, 36,
                           fill=icon_color, outline="",
                           width=0)
        # Rounded top of mic
        c.create_oval(24, 16, 40, 28,
                      fill=icon_color, outline="")

        # Mic stand arc (base)
        c.create_arc(20, 28, 44, 46,
                     start=0, extent=-180,
                     outline=icon_color,
                     style="arc", width=3)

        # Mic pole
        c.create_rectangle(30, 43, 34, 50,
                           fill=icon_color, outline="")

        # Mic base line
        c.create_rectangle(24, 49, 40, 52,
                           fill=icon_color, outline="")


    def _animate_mic_pulse(self):
        """
        Animates pulsing rings around mic button
        when listening — like Gemini's ripple effect.
        """
        if not self.is_listening:
            return

        c = self.mic_canvas
        # Remove old pulse rings
        c.delete("pulse")

        # Draw 2 expanding rings
        self.pulse_angle = (self.pulse_angle + 8) % 360
        scale = 0.5 + 0.5 * abs(math.sin(math.radians(self.pulse_angle)))

        r1 = int(32 + 10 * scale)
        r2 = int(32 + 16 * scale)
        alpha1 = int(180 * (1 - scale))
        alpha2 = int(100 * (1 - scale))

        # Pulse ring 1
        c.create_oval(32 - r1, 32 - r1, 32 + r1, 32 + r1,
                      outline=COLORS["mic_listening"],
                      width=2, tags="pulse")

        # Pulse ring 2
        c.create_oval(32 - r2, 32 - r2, 32 + r2, 32 + r2,
                      outline=COLORS["accent_blue"],
                      width=1, tags="pulse")

        # Schedule next frame (60fps feel)
        self.mic_anim_id = self.root.after(30, self._animate_mic_pulse)


    def _on_mic_hover(self, event):
        if not self.is_listening and not self.is_speaking:
            c = self.mic_canvas
            c.delete("hover")
            c.create_oval(4, 4, 60, 60,
                          outline=COLORS["accent_glow"],
                          width=1, tags="hover")


    def _on_mic_leave(self, event):
        self.mic_canvas.delete("hover")


    # ========================================================
    # WAVE ANIMATION (status bar)
    # ========================================================

    def _draw_idle_wave(self):
        """Draws a flat idle waveform in status bar."""
        c = self.wave_canvas
        c.delete("all")
        for i in range(5):
            x = 10 + i * 14
            c.create_rectangle(x, 13, x + 6, 19,
                               fill=COLORS["border"], outline="")


    def _animate_wave(self):
        """Animates speaking waveform bars."""
        if not self.is_speaking and not self.is_listening:
            self._draw_idle_wave()
            return

        c = self.wave_canvas
        c.delete("all")

        color = (COLORS["mic_listening"] if self.is_listening
                 else COLORS["accent_green"])

        import random
        for i in range(5):
            x    = 10 + i * 14
            h    = random.randint(4, 22)
            y1   = 16 - h // 2
            y2   = 16 + h // 2
            c.create_rectangle(x, y1, x + 6, y2,
                               fill=color, outline="")

        self.root.after(80, self._animate_wave)


    # ========================================================
    # CHAT MESSAGE BUILDERS
    # ========================================================

    def _add_nova_message(self, text):
        """Adds a Nova (assistant) message bubble to chat."""
        self.message_count += 1
        self._add_message_bubble(
            sender="Nova",
            text=text,
            align="left",
            bubble_color=COLORS["bubble_nova"],
            text_color=COLORS["text_primary"],
            label_color=COLORS["accent_glow"]
        )


    def _add_user_message(self, text):
        """Adds a User message bubble to chat."""
        self.message_count += 1
        self._add_message_bubble(
            sender="You",
            text=text,
            align="right",
            bubble_color=COLORS["bubble_user"],
            text_color=COLORS["text_user"],
            label_color=COLORS["accent_blue"]
        )


    def _add_message_bubble(self, sender, text, align,
                             bubble_color, text_color, label_color):
        """
        Creates a styled chat bubble widget.
        align = "left" for Nova, "right" for user.
        """

        # Outer row frame (full width)
        row = tk.Frame(self.chat_frame, bg=COLORS["bg_main"])
        row.pack(fill="x", padx=16, pady=(6, 2))

        # Timestamp
        ts = datetime.datetime.now().strftime("%I:%M %p")

        if align == "left":
            # ---- Nova bubble (left-aligned) ----

            # Avatar circle
            avatar = tk.Canvas(row, width=36, height=36,
                               bg=COLORS["bg_main"],
                               highlightthickness=0)
            avatar.pack(side="left", anchor="n", padx=(0, 10), pady=4)
            avatar.create_oval(2, 2, 34, 34,
                               fill=COLORS["accent_blue"], outline="")
            avatar.create_text(18, 18, text="N",
                               font=("Segoe UI", 13, "bold"),
                               fill="white")

            # Bubble container
            bubble_col = tk.Frame(row, bg=COLORS["bg_main"])
            bubble_col.pack(side="left", fill="x", expand=True)

            # Sender name + time
            meta = tk.Frame(bubble_col, bg=COLORS["bg_main"])
            meta.pack(anchor="w", pady=(0, 3))

            tk.Label(meta, text=ASSISTANT_NAME,
                     font=("Segoe UI", 10, "bold"),
                     fg=label_color,
                     bg=COLORS["bg_main"]).pack(side="left")

            tk.Label(meta, text=f"  {ts}",
                     font=FONT_SMALL,
                     fg=COLORS["text_secondary"],
                     bg=COLORS["bg_main"]).pack(side="left")

            # Message bubble
            bubble = tk.Frame(bubble_col,
                              bg=bubble_color,
                              padx=16, pady=12)
            bubble.pack(anchor="w")

            tk.Label(bubble, text=text,
                     font=FONT_CHAT,
                     fg=text_color,
                     bg=bubble_color,
                     wraplength=500,
                     justify="left",
                     anchor="w").pack(anchor="w")

        else:
            # ---- User bubble (right-aligned) ----

            # Bubble container on right
            bubble_col = tk.Frame(row, bg=COLORS["bg_main"])
            bubble_col.pack(side="right", fill="x")

            # Sender name + time (right-aligned)
            meta = tk.Frame(bubble_col, bg=COLORS["bg_main"])
            meta.pack(anchor="e", pady=(0, 3))

            tk.Label(meta, text=f"{ts}  ",
                     font=FONT_SMALL,
                     fg=COLORS["text_secondary"],
                     bg=COLORS["bg_main"]).pack(side="left")

            tk.Label(meta, text="You",
                     font=("Segoe UI", 10, "bold"),
                     fg=label_color,
                     bg=COLORS["bg_main"]).pack(side="left")

            # Message bubble
            bubble = tk.Frame(bubble_col,
                              bg=bubble_color,
                              padx=16, pady=12)
            bubble.pack(anchor="e")

            tk.Label(bubble, text=text,
                     font=FONT_CHAT,
                     fg=text_color,
                     bg=bubble_color,
                     wraplength=500,
                     justify="right",
                     anchor="e").pack(anchor="e")

            # Avatar
            avatar = tk.Canvas(row, width=36, height=36,
                               bg=COLORS["bg_main"],
                               highlightthickness=0)
            avatar.pack(side="right", anchor="n",
                        padx=(10, 0), pady=4)
            avatar.create_oval(2, 2, 34, 34,
                               fill=COLORS["bg_card"], outline="")
            avatar.create_text(18, 18, text="U",
                               font=("Segoe UI", 13, "bold"),
                               fill=COLORS["text_primary"])

        # Scroll to bottom after adding message
        self.root.after(50, self._scroll_to_bottom)

        # Update message count
        self.count_label.configure(
            text=f"{self.message_count} message{'s' if self.message_count != 1 else ''}"
        )


    def _add_system_message(self, text):
        """Adds a centered system/status message."""
        row = tk.Frame(self.chat_frame, bg=COLORS["bg_main"])
        row.pack(fill="x", padx=16, pady=6)

        tk.Label(
            row, text=f"── {text} ──",
            font=FONT_SMALL,
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_main"]
        ).pack()


    # ========================================================
    # SCROLL HELPERS
    # ========================================================

    def _scroll_to_bottom(self):
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)


    def _on_chat_resize(self, event):
        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox("all")
        )


    def _on_canvas_resize(self, event):
        self.chat_canvas.itemconfig(
            self.chat_window, width=event.width
        )


    def _on_mousewheel(self, event):
        self.chat_canvas.yview_scroll(
            int(-1 * (event.delta / 120)), "units"
        )


    # ========================================================
    # INPUT HANDLERS
    # ========================================================

    def _on_input_focus(self, event):
        """Clear placeholder text on focus."""
        current = self.text_input.get("1.0", "end-1c")
        if current == "Type a message or click the mic...":
            self.text_input.delete("1.0", "end")
            self.text_input.configure(fg=COLORS["text_primary"])


    def _on_input_blur(self, event):
        """Restore placeholder if empty."""
        current = self.text_input.get("1.0", "end-1c").strip()
        if not current:
            self.text_input.insert("1.0", "Type a message or click the mic...")
            self.text_input.configure(fg=COLORS["text_secondary"])


    def _on_enter_key(self, event):
        """Send message when Enter pressed (Shift+Enter for newline)."""
        if not event.state & 0x1:  # No Shift key held
            self._send_text()
            return "break"         # Prevent newline insertion


    def _send_text(self):
        """Sends typed text message to command handler."""
        text = self.text_input.get("1.0", "end-1c").strip()

        # Ignore placeholder or empty
        if not text or text == "Type a message or click the mic...":
            return

        # Clear input
        self.text_input.delete("1.0", "end")

        # Show user message
        self._add_user_message(text)

        # Process in background thread
        threading.Thread(
            target=self._handle_text_command,
            args=(text.lower(),),
            daemon=True
        ).start()


    # ========================================================
    # MIC BUTTON HANDLER
    # ========================================================

    def _on_mic_click(self, event):
        """Starts/stops listening when mic is clicked."""
        if self.is_listening or self.is_speaking or self.is_processing:
            return  # Already busy

        # Start voice listening in background thread
        threading.Thread(
            target=self._voice_listen_thread,
            daemon=True
        ).start()


    # ========================================================
    # VOICE LISTENING THREAD
    # ========================================================

    def _voice_listen_thread(self):
        """
        Runs in background thread.
        Listens to mic, converts to text,
        then calls command handler.
        """

        recognizer = sr.Recognizer()

        # Update UI: listening state
        self.msg_queue.put(("state", "listening"))

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                with sr.Microphone() as source:

                    if attempt > 1:
                        self.msg_queue.put((
                            "status",
                            f"🔄 Retry {attempt}/{MAX_RETRIES} — speak now..."
                        ))

                    recognizer.adjust_for_ambient_noise(source, duration=1)

                    audio = recognizer.listen(
                        source,
                        timeout=LISTEN_TIMEOUT,
                        phrase_time_limit=10
                    )

                # Processing state
                self.msg_queue.put(("state", "processing"))
                self.msg_queue.put(("status", "⏳ Processing your speech..."))

                text = recognizer.recognize_google(audio, language=LANGUAGE)
                text_lower = text.lower().strip()

                # Show user message in chat
                self.msg_queue.put(("user_msg", text))

                # Handle the command
                self._handle_text_command(text_lower)
                return

            except sr.UnknownValueError:
                if attempt < MAX_RETRIES:
                    self.msg_queue.put((
                        "status",
                        f"❌ Didn't catch that — trying again... ({attempt}/{MAX_RETRIES})"
                    ))
                    time.sleep(0.5)
                else:
                    self.msg_queue.put(("state", "idle"))
                    self.msg_queue.put((
                        "status",
                        "❌ Could not understand. Please try again."
                    ))
                    self._speak_and_show("Sorry, I couldn't understand that. Please try again.")

            except sr.WaitTimeoutError:
                if attempt < MAX_RETRIES:
                    self.msg_queue.put((
                        "status",
                        f"⏰ No speech detected — listening again..."
                    ))
                else:
                    self.msg_queue.put(("state", "idle"))
                    self.msg_queue.put((
                        "status", "⏰ No speech detected."
                    ))
                    self._speak_and_show("I didn't hear anything. Please try again.")

            except sr.RequestError:
                self.msg_queue.put(("state", "idle"))
                self.msg_queue.put((
                    "status", "❌ Internet error — check your connection."
                ))
                self._speak_and_show("Network error. Please check your internet connection.")
                return

            except Exception as e:
                self.msg_queue.put(("state", "idle"))
                self.msg_queue.put(("status", f"⚠️ Error: {str(e)[:40]}"))
                return

        # All retries failed
        self.msg_queue.put(("state", "idle"))


    # ========================================================
    # COMMAND HANDLER
    # ========================================================

    def _handle_text_command(self, text):
        """
        Master command handler.
        Routes text to correct action.
        Runs in background thread.
        """

        def speak_fn(msg):
            """Wrapper: speak + show in chat."""
            self._speak_and_show(msg)

        # ---- EXIT ----
        exit_words = ["exit", "quit", "bye", "goodbye",
                      "stop", "shut down", "turn off"]
        if any(word in text for word in exit_words):
            self._speak_and_show(
                "Goodbye! It was wonderful talking to you. See you soon!"
            )
            self.root.after(2000, self._on_close)
            return

        # ---- WEBSITES ----
        matched, response = open_website(text, speak_fn)
        if matched:
            return

        # ---- APPS ----
        matched, response = open_app(text, speak_fn)
        if matched:
            return

        # ---- SEARCH ----
        matched, response = handle_search(text, speak_fn)
        if matched:
            return

        # ---- TIME ----
        if "time" in text:
            tell_time(speak_fn)

        # ---- DATE ----
        elif "date" in text or "today" in text or "day is it" in text:
            tell_date(speak_fn)

        # ---- WEATHER ----
        elif "weather" in text:
            tell_weather(text, speak_fn)

        # ---- GREETING ----
        elif any(w in text for w in ["hello", "hi", "hey", "howdy"]):
            greet_user(speak_fn)

        # ---- HOW ARE YOU ----
        elif "how are you" in text:
            speak_fn("I'm running perfectly! All systems are online. How can I help you?")

        # ---- NAME ----
        elif "your name" in text or "who are you" in text:
            speak_fn(f"I am {ASSISTANT_NAME}, your personal AI voice assistant, built with Python!")

        # ---- JOKE ----
        elif "joke" in text or "funny" in text or "make me laugh" in text:
            tell_joke(speak_fn)

        # ---- FACT ----
        elif "fact" in text or "tell me something" in text or "did you know" in text:
            tell_fact(speak_fn)

        # ---- STATUS ----
        elif "status" in text or "are you there" in text:
            system_status(speak_fn)

        # ---- WHO MADE YOU ----
        elif "who made you" in text or "who created you" in text or "who built you" in text:
            speak_fn("You built me using Python! That makes you a real programmer. Well done!")

        # ---- THANKS ----
        elif "thank" in text or "thanks" in text:
            speak_fn("You're welcome! I'm always here whenever you need me.")
# ---- CLEAR CONVERSATION ----
        elif "clear conversation" in text or "forget everything" in text or "reset chat" in text:
            from ai_brain import reset_conversation
            reset_conversation()
            speak_fn("Done! I've cleared my memory. Fresh start!")

# ---- DIRECT AI QUESTION ----
        elif text.startswith("ask") or "what is" in text or "how does" in text or \
            "explain" in text or "tell me about" in text or "who is" in text or \
            "why is" in text or "when did" in text or "where is" in text:
            from ai_brain import ask_gemini
            self.msg_queue.put(("status", "🧠 Thinking with AI..."))
            ai_response = ask_gemini(text)
            speak_fn(ai_response)        
        # ---- HELP ----
        elif "help" in text or "what can you do" in text:
            speak_fn(
                "I can do lots of things! Tell you the time or date, "
                "open websites like Google, YouTube, Gmail, Netflix, and more, "
                "search Google, YouTube, or Wikipedia, "
                "open Windows apps like Notepad and Calculator, "
                "check the weather, tell jokes and fun facts — "
                "just ask me anything!"
            )

       
       # ---- UNKNOWN → ASK GEMINI AI ----
        else:
    # Import Gemini brain
         from ai_brain import ask_gemini

    # Show thinking status in UI
        self.msg_queue.put(("status", "🧠 Thinking with AI..."))
        self.msg_queue.put(("system", "Nova is thinking..."))

    # Ask Gemini for a smart answer
        ai_response = ask_gemini(text)

    # Speak and show the AI response
        speak_fn(ai_response)


    # ========================================================
    # SPEAK + SHOW IN CHAT
    # ========================================================

    def _speak_and_show(self, text):
        """
        Speaks text AND adds it to chat as Nova bubble.
        Runs in background thread safely via queue.
        """
        # Show in chat via queue (thread-safe)
        self.msg_queue.put(("nova_msg", text))
        self.msg_queue.put(("state", "speaking"))
        self.msg_queue.put(("status", f"🔊 {ASSISTANT_NAME} is speaking..."))

        # Speak it
        try:
            engine = create_tts_engine()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            pass

        # Back to idle
        self.msg_queue.put(("state", "idle"))
        self.msg_queue.put(("status", "Ready — say something or type below"))


    # ========================================================
    # QUEUE PROCESSOR (runs on main thread via after())
    # ========================================================

    def _process_queue(self):
        """
        Processes messages from background threads.
        Runs on main UI thread — safe to update widgets.
        """
        try:
            while True:
                msg_type, data = self.msg_queue.get_nowait()

                # ---- State changes ----
                if msg_type == "state":
                    self._set_state(data)

                # ---- Status bar text ----
                elif msg_type == "status":
                    self.status_label.configure(text=data)

                # ---- Nova chat bubble ----
                elif msg_type == "nova_msg":
                    self._add_nova_message(data)

                # ---- User chat bubble ----
                elif msg_type == "user_msg":
                    self._add_user_message(data)

                # ---- System message ----
                elif msg_type == "system":
                    self._add_system_message(data)

        except queue.Empty:
            pass

        # Schedule next check (every 50ms)
        if self.running:
            self.root.after(50, self._process_queue)


    def _set_state(self, state):
        """
        Updates UI elements based on assistant state.
        States: idle, listening, processing, speaking
        """
        if state == "listening":
            self.is_listening   = True
            self.is_processing  = False
            self.is_speaking    = False
            self._draw_mic_button("listening")
            self._animate_mic_pulse()
            self._animate_wave()
            self.status_pill.configure(
                text="● Listening",
                fg=COLORS["mic_listening"]
            )
            self.status_label.configure(
                text="🎤 Listening — speak now!"
            )

        elif state == "processing":
            self.is_listening   = False
            self.is_processing  = True
            self.is_speaking    = False
            self._draw_mic_button("processing")
            self.status_pill.configure(
                text="● Processing",
                fg=COLORS["mic_processing"]
            )

        elif state == "speaking":
            self.is_listening   = False
            self.is_processing  = False
            self.is_speaking    = True
            self._draw_mic_button("speaking")
            self._animate_wave()
            self.status_pill.configure(
                text="● Speaking",
                fg=COLORS["accent_green"]
            )

        elif state == "idle":
            self.is_listening   = False
            self.is_processing  = False
            self.is_speaking    = False
            # Cancel pulse animation
            if self.mic_anim_id:
                self.root.after_cancel(self.mic_anim_id)
                self.mic_anim_id = None
            self._draw_mic_button("idle")
            self._draw_idle_wave()
            self.status_pill.configure(
                text="● Ready",
                fg=COLORS["accent_green"]
            )


    # ========================================================
    # UTILITY
    # ========================================================

    def _clear_chat(self):
        """Clears all chat messages."""
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        self.message_count = 0
        self.count_label.configure(text="0 messages")
        self._add_system_message("Chat cleared")
        self._add_nova_message("Chat cleared! How can I help you?")


    def _on_close(self):
        """Gracefully shuts down the application."""
        self.running = False
        self.root.quit()
        self.root.destroy()


# ============================================================
# MAIN — LAUNCH NOVA
# ============================================================

def main():
    """Creates the Tkinter window and launches Nova."""

    root = tk.Tk()

    # ---- Window icon (colored title bar) ----
    root.configure(bg=COLORS["bg_main"])

    # ---- DPI awareness for sharp fonts on Windows ----
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    # ---- Launch app ----
    app = NovaApp(root)

    # ---- Start Tkinter event loop ----
    root.mainloop()


if __name__ == "__main__":
    main()