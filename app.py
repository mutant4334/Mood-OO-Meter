import streamlit as st
import json
import os
import streamlit.components.v1 as components

# ---------- Configuration ---------- #
MOOD_FILE = "moods_data.json"
MOODS = {
    "happy": "😊 Happy",
    "sad": "😢 Sad",
    "angry": "😠 Angry",
    "calm": "😌 Calm"
}
COLORS = {
    "happy": "#FFB6C1",   # Pink
    "sad": "#ADD8E6",     # Light Blue
    "angry": "#FFA07A",   # Light Salmon
    "calm": "#90EE90"     # Light Green
}

# ---------- Initialize Mood Data ---------- #
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

# ---------- Page Setup ---------- #
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🧠 Mood-O-Meter</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Tap any quadrant to record your mood anonymously</h3>", unsafe_allow_html=True)

# ---------- Inject Hidden Input Field ---------- #
mood_selected = st.experimental_get_query_params().get("mood", [None])[0]

# ---------- Render Quadrants with JS ---------- #
html_code = f"""
<div style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; height: 70vh; width: 100vw; cursor:pointer;">
    <div onclick="window.location.search='?mood=happy'" style="background-color:{COLORS['happy']}; display:flex; align-items:center; justify-content:center; font-size:2em; font-weight:bold; border:2px solid white;">{MOODS['happy']}</div>
    <div onclick="window.location.search='?mood=sad'" style="background-color:{COLORS['sad']}; display:flex; align-items:center; justify-content:center; font-size:2em; font-weight:bold; border:2px solid white;">{MOODS['sad']}</div>
    <div onclick="window.location.search='?mood=angry'" style="background-color:{COLORS['angry']}; display:flex; align-items:center; justify-content:center; font-size:2em; font-weight:bold; border:2px solid white;">{MOODS['angry']}</div>
    <div onclick="window.location.search='?mood=calm'" style="background-color:{COLORS['calm']}; display:flex; align-items:center; justify-content:center; font-size:2em; font-weight:bold; border:2px solid white;">{MOODS['calm']}</div>
</div>
"""

components.html(html_code, height=550)

# ---------- Handle Mood Click ---------- #
if mood_selected in MOODS:
    mood_data[mood_selected] += 1
    save_data(mood_data)
    st.success(f"✅ Thanks! Your mood '{MOODS[mood_selected]}' was recorded.")
    st.experimental_set_query_params()  # Clear mood from URL
