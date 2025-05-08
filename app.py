import streamlit as st
import json
import os

# ---------- Configuration ---------- #
MOOD_FILE = "moods_data.json"
MOODS = {
    "top-left": ("😊 Happy", "#FFB6C1"),
    "top-right": ("😢 Sad", "#ADD8E6"),
    "bottom-left": ("😠 Angry", "#FFA07A"),
    "bottom-right": ("😌 Calm", "#90EE90")
}

# ---------- Initialize Data ---------- #
def initialize_data():
    if not os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, "w") as f:
            json.dump({label: 0 for label in MOODS.keys()}, f)

def load_data():
    with open(MOOD_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(MOOD_FILE, "w") as f:
        json.dump(data, f)

# ---------- Start App ---------- #
st.set_page_config(page_title="Mood Quadrant", layout="wide")
initialize_data()
mood_data = load_data()

# ---------- Layout ---------- #
st.markdown(
    """
    <style>
    .quad-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        height: 70vh;
        width: 100%;
        gap: 10px;
    }
    .quad {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8em;
        font-weight: bold;
        color: #000000;
        border-radius: 12px;
        cursor: pointer;
    }
    .top-left { background-color: #FFB6C1; }
    .top-right { background-color: #ADD8E6; }
    .bottom-left { background-color: #FFA07A; }
    .bottom-right { background-color: #90EE90; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧠 Mood-O-Meter")
st.markdown("### Tap your current mood:")

# ---------- Quadrant Buttons (Using HTML + Streamlit Buttons) ---------- #
col1, col2 = st.columns(2)
with col1:
    if st.button("😊 Happy", key="top-left"):
        mood_data["top-left"] += 1
        save_data(mood_data)
        st.success("Thanks for your response: 😊 Happy")

with col2:
    if st.button("😢 Sad", key="top-right"):
        mood_data["top-right"] += 1
        save_data(mood_data)
        st.success("Thanks for your response: 😢 Sad")

col3, col4 = st.columns(2)
with col3:
    if st.button("😠 Angry", key="bottom-left"):
        mood_data["bottom-left"] += 1
        save_data(mood_data)
        st.success("Thanks for your response: 😠 Angry")

with col4:
    if st.button("😌 Calm", key="bottom-right"):
        mood_data["bottom-right"] += 1
        save_data(mood_data)
        st.success("Thanks for your response: 😌 Calm")

# ---------- Optional: Display Totals ---------- #
with st.expander("📊 Mood Count Summary"):
    for k, (label, _) in MOODS.items():
        st.write(f"{label}: {mood_data[k]}")
