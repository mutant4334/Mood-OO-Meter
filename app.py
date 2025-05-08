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

# ---------- Page Settings ---------- #
st.set_page_config(layout="wide")
st.title("🧠 Mood-O-Meter")
st.markdown("### Tap a quadrant to record your mood anonymously")

# ---------- Render 2x2 Quadrant UI ---------- #
html_code = f"""
<div style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; height: 60vh; width: 100vw;">
    <div onclick="sendMood('happy')" style="background-color:{COLORS['happy']}; display:flex; align-items:center; justify-content:center; font-size:2em; font-weight:bold; border:2px solid white;">{MOODS['happy']}</div>
    <div onclick="sendMood('sad')" style="background-color:{COLORS['sad']}; display:flex; align-items:center; justify-content:center; font-size:2em; font-weight:bold; border:2px solid white;">{MOODS['sad']}</div>
    <div onclick="sendMood('angry')" style="background-color:{COLORS['angry']}; display:flex; align-items:center; justify-content:center; font-size:2em; font-weight:bold; border:2px solid white;">{MOODS['angry']}</div>
    <div onclick="sendMood('calm')" style="background-color:{COLORS['calm']}; display:flex; align-items:center; justify-content:center; font-size:2em; font-weight:bold; border:2px solid white;">{MOODS['calm']}</div>
</div>

<script>
    const moodInput = window.parent.document.querySelector("input[name='mood_input']")
    function sendMood(mood) {{
        moodInput.value = mood;
        moodInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
    }}
</script>
"""

# ---------- Hidden Communication with JS ---------- #
mood_selected = st.text_input("mood_input", label_visibility="collapsed")
components.html(html_code, height=500)

# ---------- Handle Mood Response ---------- #
if mood_selected and mood_selected in MOODS:
    mood_data[mood_selected] += 1
    save_data(mood_data)
    st.success(f"✅ Thanks! Your mood '{MOODS[mood_selected]}' was recorded anonymously.")
    st.experimental_rerun()

# ---------- Mood Summary (Optional) ---------- #
with st.expander("📊 View Mood Summary"):
    for mood, count in mood_data.items():
        st.write(f"{MOODS[mood]}: {count}")
