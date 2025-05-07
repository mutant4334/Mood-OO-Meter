import streamlit as st
import json
import os
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt

# File paths
MOOD_FILE = "moods_data.json"
LOTTIE_FILE = "eleven_moods.json"

# Mood options with emojis
MOODS = [
    "😊 Happy", "😢 Sad", "😠 Angry", "🤩 Excited", "😰 Anxious",
    "😮 Surprised", "🥱 Bored", "😕 Confused", "❤️ Loved", "🙏 Grateful", "😌 Calm"
]

# Load Lottie file
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Initialize mood data if not exists
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w") as f:
        json.dump({mood: 0 for mood in MOODS}, f)

# Load mood data
with open(MOOD_FILE, "r") as f:
    mood_data = json.load(f)

# Page configuration
st.set_page_config(page_title="Mood Cradle", layout="centered")
st.title("🧠 Newton's Cradle Mood Survey")
st.markdown("Tap your current **mood** and contribute to the collective vibes ✨")

# Show Lottie animation
lottie_animation = load_lottiefile(LOTTIE_FILE)
st_lottie(lottie_animation, speed=1, loop=True, height=250)

# Tappable mood buttons
st.subheader("👇 Tap your current mood:")
cols = st.columns(4)  # 4 buttons per row
clicked = False

for i, mood in enumerate(MOODS):
    if cols[i % 4].button(mood):
        mood_data[mood] += 1
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_data, f)
        st.success(f"✅ Mood '{mood}' captured!")
        clicked = True
        break

# Mood distribution chart
st.subheader("📊 Collective Mood Vibes")
fig, ax = plt.subplots()
ax.bar(mood_data.keys(), mood_data.values(), color='skyblue')
ax.set_ylabel("Responses")
ax.set_title("Mood Distribution")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Footer
st.caption("🧪 Built with Streamlit | ⚙️ Data is anonymous & updates in real-time.")
