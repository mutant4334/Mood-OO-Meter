import streamlit as st
import matplotlib.pyplot as plt
import json
import os
import base64

# ---------- CONFIG ----------
MOOD_FILE = "moods_data.json"
PASSWORD = "owner@123"  # Change this to your secret password
BG_IMAGE = "background.jpg"

MOODS = {
    0: "😊 Happy",
    1: "😢 Sad",
    2: "😠 Angry",
    3: "🤩 Excited",
    4: "😌 Calm"
}

# ---------- CSS ----------
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: #fff;
    }}
    .title {{
        font-size: 2.5rem;
        font-weight: bold;
        color: #f8f9fa;
        text-align: center;
        margin-bottom: 10px;
    }}
    .subtitle {{
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 30px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------- FILE INIT ----------
if not os.path.exists(MOOD_FILE):
    with open(MOOD_FILE, "w") as f:
        json.dump({str(k): 0 for k in MOODS}, f)

with open(MOOD_FILE, "r") as f:
    mood_data = json.load(f)

# ---------- APP UI ----------
st.set_page_config("Mood Cradle", layout="centered")
set_background(BG_IMAGE)

st.markdown('<div class="title">🧠 Mood Cradle</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tap how you feel today 💬</div>', unsafe_allow_html=True)

# ---------- Mood Pie Selection ----------
fig, ax = plt.subplots()
labels = [MOODS[int(k)] for k in mood_data.keys()]
sizes = [mood_data[k] for k in mood_data.keys()]
colors = ['#f4a261', '#2a9d8f', '#e76f51', '#e9c46a', '#a8dadc']
explode = [0.1 if k == max(mood_data, key=int) else 0 for k in mood_data.keys()]
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode)
ax.axis('equal')
st.pyplot(fig)

st.markdown("### Select your mood:")
cols = st.columns(len(MOODS))

for i, mood in MOODS.items():
    if cols[i].button(mood):
        mood_data[str(i)] += 1
        with open(MOOD_FILE, "w") as f:
            json.dump(mood_data, f)
        st.success(f"✅ You selected: {mood}")
        st.balloons()

# ---------- Admin View (Results) ----------
st.markdown("---")
with st.expander("🔒 Owner Access: View & Reset Results"):
    pw = st.text_input("Enter password", type="password")
    if pw == PASSWORD:
        st.success("Access granted.")
        st.markdown("### 📊 Current Mood Data:")
        for i in MOODS:
            st.write(f"{MOODS[i]}: {mood_data[str(i)]}")

        st.markdown("#### 🔁 Reset Data?")
        if st.button("Reset All Data"):
            with open(MOOD_FILE, "w") as f:
                json.dump({str(k): 0 for k in MOODS}, f)
            st.success("All mood data has been reset.")
    elif pw:
        st.error("Incorrect password.")
