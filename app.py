import streamlit as st
import json
import os

# Configuration
MOOD_FILE = "moods_data.json"
PASSWORD = "owner123"
MOODS = {
    "happy": "😊 Happy",
    "sad": "😢 Sad",
    "angry": "😠 Angry",
    "calm": "😌 Calm"
}
COLORS = {
    "happy": "#FFB6C1",
    "sad": "#ADD8E6",
    "angry": "#FFA07A",
    "calm": "#90EE90"
}

# Initialize mood file
def initialize_data():
    if not os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, "w") as f:
            json.dump({m: 0 for m in MOODS}, f)

def load_data():
    with open(MOOD_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(MOOD_FILE, "w") as f:
        json.dump(data, f)

initialize_data()
mood_data = load_data()

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🧠 Mood-O-Meter</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Click any colored quadrant to record your mood</h4>", unsafe_allow_html=True)

# Handle mood selection
if "selected_mood" not in st.session_state:
    st.session_state["selected_mood"] = None

def mood_box(mood_key):
    color = COLORS[mood_key]
    label = MOODS[mood_key]
    with st.form(f"form_{mood_key}"):
        st.markdown(
            f"""
            <button style='height:200px; width:100%; background-color:{color}; border:none; border-radius:10px;
                    font-size:24px; font-weight:bold; cursor:pointer'>
                {label}
            </button>
            """,
            unsafe_allow_html=True
        )
        submitted = st.form_submit_button("")
        if submitted:
            st.session_state["selected_mood"] = mood_key
            mood_data[mood_key] += 1
            save_data(mood_data)

# Display 2x2 quadrants as buttons
row1 = st.columns(2)
with row1[0]:
    mood_box("happy")
with row1[1]:
    mood_box("sad")

row2 = st.columns(2)
with row2[0]:
    mood_box("angry")
with row2[1]:
    mood_box("calm")

# Confirmation
if st.session_state["selected_mood"]:
    mood = st.session_state["selected_mood"]
    st.success(f"✅ You selected: {MOODS[mood]}")

# Admin section
with st.expander("🔒 View Mood Summary"):
    password = st.text_input("Enter password to view results:", type="password")
    if password == PASSWORD:
        st.subheader("📊 Mood Count")
        mood_data = load_data()
        for mood, count in mood_data.items():
            st.markdown(
                f"<div style='background-color:{COLORS[mood]}; padding:10px; margin:5px; border-radius:5px;'>"
                f"<strong>{MOODS[mood]}</strong>: {count}</div>",
                unsafe_allow_html=True
            )
        if st.button("🔁 Reset All Moods"):
            save_data({m: 0 for m in MOODS})
            st.success("✅ Mood counts reset.")
    elif password:
        st.error("❌ Incorrect password.")
