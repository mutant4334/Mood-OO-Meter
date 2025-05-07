import streamlit as st
import json
import os
import matplotlib.pyplot as plt
import base64

# ---------- Config ---------- #
PASSWORD = "wheyprotein"  # 🔒 Change this password
MOOD_FILE = "moods_data.json"
BG_IMAGE = "background.jpg"

MOODS = {
    0: "😊 Happy",
    1: "😢 Sad",
    2: "😠 Angry",
    3: "😌 Calm",
    4: "❤️ Loved"
}

# ---------- CSS for Background ---------- #
def set_bg_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2em;
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- Utility Functions ---------- #
def initialize_data():
    if not os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, "w") as f:
            json.dump({str(k): 0 for k in MOODS.keys()}, f)

def load_data():
    with open(MOOD_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(MOOD_FILE, "w") as f:
        json.dump(data, f)

# ---------- App Starts ---------- #
st.set_page_config(page_title="Mood-O-Meter", layout="centered")
initialize_data()

if os.path.exists(BG_IMAGE):
    set_bg_image(BG_IMAGE)

st.title("Mood-O-Meter")
st.markdown("### How are you feeling today?")

# Realtime mood submission
mood_data = load_data()
cols = st.columns(5)

for i in MOODS:
    if cols[i].button(MOODS[i]):
        mood_data[str(i)] += 1
        save_data(mood_data)
        st.success(f"Thanks! Your response was recorded anonymously as '{MOODS[i]}'")
        st.rerun()

# ---------- Password-Protected Live View ---------- #
with st.expander("🔒 View Live Results (Password Protected)"):
    password_input = st.text_input("Enter password:", type="password")
    if password_input == PASSWORD:
        st.subheader("📊 Mood Distribution (Realtime)")

        mood_data = load_data()
        labels = [MOODS[int(k)] for k in mood_data.keys()]
        values = [mood_data[k] for k in mood_data.keys()]

        filtered = [(label, value) for label, value in zip(labels, values) if value > 0]
        if filtered:
            labels, values = zip(*filtered)

            fig, ax = plt.subplots()
            ax.barh(labels, values, color="skyblue")
            ax.set_xlabel("Votes")
            ax.set_title("Current Mood Status")
            st.pyplot(fig)
        else:
            st.info("No mood data available yet.")
    elif password_input:
        st.error("❌ Incorrect password.")

# ---------- Developer Tools (Standalone) ---------- #
st.markdown("### 🛠️ Developer Tools")
dev_pass = st.text_input("Enter dev password to reset data:", type="password", key="dev_pass")
if dev_pass == PASSWORD:
    if st.button("🔁 Reset All Data"):
        save_data({str(k): 0 for k in MOODS.keys()})
        st.success("All mood data has been reset.")

# ---------- Footer ---------- #
st.markdown("---")
st.markdown("**Team Culture | Leadership Development | Talent**")
