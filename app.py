import streamlit as st
import json
import os

# Constants
MOOD_FILE = "moods_data.json"
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
st.markdown("<h4 style='text-align: center;'>Tap any quadrant to record your current mood</h4>", unsafe_allow_html=True)

# Session state for real-time updates
if "selected_mood" not in st.session_state:
    st.session_state["selected_mood"] = None

# Function to handle quadrant button clicks and update mood data
def quadrant_button(mood_key):
    color = COLORS.get(mood_key, "#FFFFFF")  # Default to white if the key is not found
    label = MOODS.get(mood_key, "Unknown Mood")  # Default to "Unknown Mood" if the key is not found
    if st.button(label, key=mood_key, help=label, use_container_width=True):
        st.session_state["selected_mood"] = mood_key
        mood_data[mood_key] += 1
        save_data(mood_data)

# Layout: 2x2 responsive on mobile only
st.markdown(
    """
    <style>
    .quadrant-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin-top: 20px;
        padding: 10px;
    }
    
    .quadrant-button {
        width: 100%;
        height: 150px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        cursor: pointer;
    }

    @media screen and (max-width: 600px) {
        .quadrant-container {
            grid-template-columns: repeat(2, 1fr);
            grid-gap: 15px;
        }

        .quadrant-button {
            font-size: 18px;
            height: 120px;
        }
    }
    </style>
    """, unsafe_allow_html=True
)

# Create Quadrants in 2x2 grid using the CSS class `quadrant-container`
st.markdown('<div class="quadrant-container">', unsafe_allow_html=True)

# Quadrant Buttons
for mood_key in MOODS:
    if st.button(MOODS[mood_key], key=mood_key, help=MOODS[mood_key], use_container_width=True):
        st.session_state["selected_mood"] = mood_key
        mood_data[mood_key] += 1
        save_data(mood_data)

st.markdown('</div>', unsafe_allow_html=True)

# Show selected mood
if st.session_state["selected_mood"]:
    mood = st.session_state["selected_mood"]
    st.success(f"✅ You selected: {MOODS[mood]}")

# Admin Section (for mood statistics, no identifiers needed)
with st.expander("🔒 View Mood Summary"):
    password = st.text_input("Enter password to view results:", type="password")
    if password == "owner123":  # Use the desired password for admin access
        st.subheader("📊 Mood Count")
        mood_data = load_data()
        for mood, count in mood_data.items():
            st.markdown(
                f"<div style='background-color:{COLORS.get(mood, '#FFFFFF')}; padding:10px; margin:5px; border-radius:5px;'>"
                f"<strong>{MOODS.get(mood, 'Unknown Mood')}</strong>: {count}</div>",
                unsafe_allow_html=True
            )
        if st.button("🔁 Reset All Moods"):
            save_data({m: 0 for m in MOODS})
            st.success("✅ Mood counts reset.")
    elif password:
        st.error("❌ Incorrect password.")
