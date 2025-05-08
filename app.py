import streamlit as st
import json
import os
import matplotlib.pyplot as plt

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

# Load current mood data
mood_data = load_data()

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🧠 Mood-O-Meter</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Click a quadrant to record your mood</h3>", unsafe_allow_html=True)

# State variable to track mood selection
if "mood_selected" not in st.session_state:
    st.session_state["mood_selected"] = None

# Create 4 quadrant layout using columns
col1, col2 = st.columns(2)

with col1:
    if st.button(MOODS["happy"], use_container_width=True):
        st.session_state["mood_selected"] = "happy"
        mood_data["happy"] += 1
        save_data(mood_data)
    if st.button(MOODS["angry"], use_container_width=True):
        st.session_state["mood_selected"] = "angry"
        mood_data["angry"] += 1
        save_data(mood_data)

with col2:
    if st.button(MOODS["sad"], use_container_width=True):
        st.session_state["mood_selected"] = "sad"
        mood_data["sad"] += 1
        save_data(mood_data)
    if st.button(MOODS["calm"], use_container_width=True):
        st.session_state["mood_selected"] = "calm"
        mood_data["calm"] += 1
        save_data(mood_data)

# Show confirmation
if st.session_state["mood_selected"]:
    mood = st.session_state["mood_selected"]
    st.success(f"✅ Your mood '{MOODS[mood]}' has been recorded.")

# Developer/admin results section
with st.expander("🔒 View Live Results"):
    password = st.text_input("Enter password to view results:", type="password")
    if password == PASSWORD:
        st.subheader("📊 Mood Distribution")
        mood_data = load_data()
        labels = [MOODS[m] for m in MOODS]
        values = [mood_data.get(m, 0) for m in MOODS]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values, color=[COLORS[m] for m in MOODS])
        ax.set_ylabel("Votes")
        ax.set_title("Mood Counts")
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, int(yval), ha='center', va='bottom')

        st.pyplot(fig)

        if st.button("🔁 Reset All Responses"):
            save_data({m: 0 for m in MOODS})
            st.success("✅ Mood responses have been reset.")
    elif password:
        st.error("❌ Incorrect password.")
