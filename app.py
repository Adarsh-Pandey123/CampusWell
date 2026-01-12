import streamlit as st
from datetime import datetime
import random
from groq import Groq

# ================== CONFIG ==================
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"

# ================== UI SETUP ==================
st.set_page_config(page_title="CampusWell", page_icon="💙")
st.title("💙 CampusWell – Student Wellness Companion")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

with st.sidebar:
    st.header("👤 Profile")
    username = st.text_input("Your name", "Student")

    st.markdown("### About")
    st.write(
        "CampusWell is designed for students to manage stress, "
        "exam pressure, and emotional challenges using AI. It offers empathetic chat, "
        "breathing exercises, daily tips, and a mood log to help students stay balanced."
    )

    st.divider()
    st.header("📊 Mood Log")
    if st.session_state.mood_log:
        for t, m in st.session_state.mood_log[-5:]:
            st.write(f"**{t}** — {m}")
    else:
        st.write("No moods recorded yet.")

    st.divider()
    if st.button("📄 Export Chat"):
        lines = [f"{r}: {t}" for r, t in st.session_state.messages]
        st.download_button(
            "Download chat.txt",
            "\n".join(lines),
            file_name="campuswell_chat.txt"
        )

    st.divider()
    st.caption("Developed by **ADARSH KUMAR PANDEY**")

# ================== HELPER FUNCTIONS ==================
def ai_reply(user_text):
    prompt = f"""You are CampusWell, a supportive mental health companion for college students.
Be empathetic, concise, and encouraging. Address {username} by name when possible.
Offer one small actionable tip suitable for students.

User says: {user_text}
"""
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL_NAME,
        )
        return chat.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def detect_mood(text):
    t = text.lower()
    if any(w in t for w in ["sad", "low", "cry"]):
        return "😔 Sad"
    if any(w in t for w in ["stress", "exam", "anxious"]):
        return "😰 Stressed"
    if any(w in t for w in ["happy", "great", "good"]):
        return "😊 Happy"
    return "😐 Neutral"

# ================== CHAT INTERFACE ==================
for role, text in st.session_state.messages:
    with st.chat_message("user" if role == "You" else "assistant"):
        st.markdown(text)

if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append(("You", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    current_mood = detect_mood(prompt)
    st.session_state.mood_log.append((datetime.now().strftime("%H:%M"), current_mood))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ai_reply(prompt)
            st.markdown(reply)
            st.session_state.messages.append(("CampusWell", reply))

# ================== SUPPORT BUTTONS ==================
st.divider()
cols = st.columns(4)

if cols[0].button("🫁 Breathing"):
    msg = "Inhale for 4s, Hold for 4s, Exhale for 6s. Repeat 3 times."
    st.session_state.messages.append(("CampusWell", msg))
    st.rerun()

if cols[1].button("💡 Daily Tip"):
    tips = [
        "Drink water before your next study session.",
        "Try the Pomodoro method: 25 minutes study, 5 minutes break.",
        "Take a 5-minute walk to refresh your mind."
    ]
    st.session_state.messages.append(("CampusWell", random.choice(tips)))
    st.rerun()

if cols[2].button("📚 Exam Mode"):
    st.session_state.messages.append(
        ("CampusWell", "Focus on one topic for 20 minutes, then take a 5-minute break. Repeat 3 times.")
    )
    st.rerun()

if cols[3].button("✨ Motivation"):
    quotes = [
        "Small steps every day lead to big results.",
        "You are capable of more than you think.",
        "Progress, not perfection.",
        "Your future self will thank you for today’s effort."
    ]
    st.session_state.messages.append(("CampusWell", random.choice(quotes)))
    st.rerun()
