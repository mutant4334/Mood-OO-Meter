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
    "happy": "#FFB6C1",   # Light Pink
    "sad": "#ADD8E6",     # Light Blue
    "angry": "#FFA07A",   # Light Salmon
    "calm": "#90EE90"     # Light Green
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

# Load current mood data
mood_data = load_data()

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🧠 Mood-O-Meter</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Tap a quadrant to record your mood</h4>", unsafe_allow_html=True)

if "mood_selected" not in st.session_state:
    st.session_state["mood_selected"] = None

# Layout for 2x2 quadrant buttons
col1, col2 = st.columns(2)

with col1:
    if st.button(MOODS["happy"], use_container_width=True):
        st.session_state["mood_selected"] = "happy"
        mood_data["happy"] += 1
        save_data(mood_data)

    st.markdown(
        f"<div style='height:200px; background-color:{COLORS['happy']}; border-radius:10px;'></div>",
        unsafe_allow_html=True
    )

    if st.button(MOODS["angry"], use_container_width=True):
        st.session_state["mood_selected"] = "angry"
        mood_data["angry"] += 1
        save_data(mood_data)

    st.markdown(
        f"<div style='height:200px; background-color:{COLORS['angry']}; border-radius:10px;'></div>",
        unsafe_allow_html=True
    )

with col2:
    if st.button(MOODS["sad"], use_container_width=True):
        st.session_state["mood_selected"] = "sad"
        mood_data["sad"] += 1
        save_data(mood_data)

    st.markdown(
        f"<div style='height:200px; background-color:{COLORS['sad']}; border-radius:10px;'></div>",
        unsafe_allow_html=True
    )

    if st.button(MOODS["calm"], use_container_width=True):
        st.session_state["mood_selected"] = "calm"
        mood_data["calm"] += 1
        save_data(mood_data)

    st.markdown(
        f"<div style='height:200px; background-color:{COLORS['calm']}; border-radius:10px;'></div>",
        unsafe_allow_html=True
    )

# Confirmation
if st.session_state["mood_selected"]:
    mood = st.session_state["mood_selected"]
    st.success(f"✅ Your mood '{MOODS[mood]}' has been recorded.")

# Admin section for results
with st.expander("🔒 View Mood Summary"):
    password = st.text_input("Enter password to view results:", type="password")
    if password == PASSWORD:
        mood_data = load_data()
        st.subheader("📊 Mood Count")
        for mood, count in mood_data.items():
            st.markdown(f"<div style='background-color:{COLORS[mood]}; padding:10px; margin:5px; border-radius:5px;'>"
                        f"<strong>{MOODS[mood]}</strong>: {count}</div>", unsafe_allow_html=True)

        if st.button("🔁 Reset All Moods"):
            save_data({m: 0 for m in MOODS})
            st.success("✅ All mood counts reset.")
    elif password:
        st.error("❌ Incorrect password.")
