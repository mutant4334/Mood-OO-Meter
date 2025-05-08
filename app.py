import streamlit as st
import json
import os

# Constants
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

# Initialize or load mood data
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

# Streamlit Page Setup
st.set_page_config(layout="wide")
st.markdown("<h2 style='text-align: center;'>🧠 Mood-O-Meter</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Tap any quadrant to record your current mood</h4>", unsafe_allow_html=True)

# Session state
if "selected_mood" not in st.session_state:
    st.session_state["selected_mood"] = None

# Create Quadrant Button
def quadrant_button(mood_key):
    color = COLORS[mood_key]
    label = MOODS[mood_key]
    with st.form(f"form_{mood_key}"):
        st.markdown(f"""
            <button style='width: 100%; height: 180px; background-color: {color}; 
            font-size: 22px; font-weight: bold; border: none; border-radius: 12px; cursor: pointer;'>
                {label}
            </button>
        """, unsafe_allow_html=True)
        submit = st.form_submit_button("")
        if submit:
            st.session_state["selected_mood"] = mood_key
            mood_data[mood_key] += 1
            save_data(mood_data)

# Layout: 2x2 responsive on all devices
col1, col2 = st.columns(2)
with col1:
    quadrant_button("happy")
with col2:
    quadrant_button("sad")

col3, col4 = st.columns(2)
with col3:
    quadrant_button("angry")
with col4:
    quadrant_button("calm")

# Show selected mood
if st.session_state["selected_mood"]:
    mood = st.session_state["selected_mood"]
    st.success(f"✅ You selected: {MOODS[mood]}")

# Admin Section
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

