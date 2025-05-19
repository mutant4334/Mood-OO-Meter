import streamlit as st
import json
import os

# Constants
MOOD_FILE = "moods_data.json"
MOODS = {
    "high_energy_unpleasant": "😠 High Energy Unpleasant",
    "high_energy_pleasant": "😄 High Energy Pleasant",
    "low_energy_unpleasant": "😞 Low Energy Unpleasant",
    "low_energy_pleasant": "😊 Low Energy Pleasant"
}
COLORS = {
    "high_energy_unpleasant": "#FFA07A",  # Light Salmon
    "high_energy_pleasant": "#90EE90",    # Light Green
    "low_energy_unpleasant": "#ADD8E6",   # Light Blue
    "low_energy_pleasant": "#FFB6C1"      # Light Pink
}

# Initialize or load mood data, and fix keys if needed
def initialize_data():
    if not os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, "w") as f:
            json.dump({m: 0 for m in MOODS}, f)
    else:
        with open(MOOD_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        if set(data.keys()) != set(MOODS.keys()):
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
st.markdown("<h4 style='text-align: center;'>How are you feeling today?</h4>", unsafe_allow_html=True)

# Session state for real-time updates
if "selected_mood" not in st.session_state:
    st.session_state["selected_mood"] = None

# CSS styling
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
        transition: all 0.3s ease-in-out;
    }
    .quadrant-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
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
    .reset-button {
        background-color: #f44b42;
        color: white;
        padding: 10px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
    }
    .reset-button:hover {
        background-color: #e0372e;
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .selected-mood {
        padding: 10px;
        font-size: 18px;
        color: #444;
        background-color: #ffffff;
        border-radius: 10px;
        margin-top: 20px;
        border: 1px solid #d1d1d1;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

# Quadrant buttons layout
st.markdown('<div class="quadrant-container">', unsafe_allow_html=True)

for mood_key in MOODS:
    label = MOODS[mood_key]
    color = COLORS.get(mood_key, "#FFFFFF")
    # Use st.button with key and help, but style is handled by CSS
    if st.button(label, key=mood_key, help=label, use_container_width=True):
        st.session_state["selected_mood"] = mood_key
        if mood_key in mood_data:
            mood_data[mood_key] += 1
            save_data(mood_data)
        else:
            st.error("⚠️ Invalid mood key selected.")

st.markdown('</div>', unsafe_allow_html=True)

# Show selected mood
if st.session_state["selected_mood"]:
    mood = st.session_state["selected_mood"]
    st.markdown(f"<div class='selected-mood'>✅ You selected: {MOODS[mood]}</div>", unsafe_allow_html=True)

# Admin Section (for mood statistics)
with st.expander("🔒 View Mood Summary"):
    password = st.text_input("Enter password to view results:", type="password")
    if password == "owner123":  # Admin password
        st.subheader("📊 Mood Count")
        mood_data = load_data()
        for mood, count in mood_data.items():
            st.markdown(
                f"<div style='background-color:{COLORS.get(mood, '#FFFFFF')}; padding:10px; margin:5px; border-radius:5px;'>"
                f"<strong>{MOODS.get(mood, 'Unknown Mood')}</strong>: {count}</div>",
                unsafe_allow_html=True
            )
        if st.button("🔁 Reset All Moods", key="reset", help="Reset all mood counts", use_container_width=True):
            save_data({m: 0 for m in MOODS})
            st.success("✅ Mood counts reset.")
    elif password:
        st.error("❌ Incorrect password.")

st.markdown("---")
st.markdown("**Team Culture | Leadership Development | Talent**")
