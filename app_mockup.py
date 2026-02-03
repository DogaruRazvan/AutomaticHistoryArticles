import streamlit as st
import json
import os
from schema.models import EventList

st.set_page_config(layout="centered", page_title="History Gold", page_icon="📜")

# CSS pentru un look modern de mobil
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-card { background: #1a1c23; border-radius: 20px; padding: 20px; border: 1px solid #333; }
    .gold-text { color: #ffd700; font-weight: bold; }
    .stImage img { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)


def load_data():
    archive_dir = "archive"
    if not os.path.exists(archive_dir) or not os.listdir(archive_dir):
        try:
            with open("output.json", "r", encoding="utf-8") as f:
                return EventList.model_validate(json.load(f))
        except:
            return None

    files = sorted(os.listdir(archive_dir), reverse=True)
    st.sidebar.title("📚 Istoric")
    selected = st.sidebar.selectbox("Alege Data:", files,
                                    format_func=lambda x: x.replace("history_", "").replace(".json", ""))

    with open(os.path.join(archive_dir, selected), "r", encoding="utf-8") as f:
        return EventList.model_validate(json.load(f))


data = load_data()

if data and data.events:
    event = data.events[0]

    # --- GALERIE FOTO ---
    # Verificăm dacă avem gallery sau doar image_url
    pics = event.gallery if (hasattr(event, 'gallery') and event.gallery) else (
        [event.image_url] if event.image_url else [])

    if pics:
        st.image(pics[0], use_container_width=True)
        if len(pics) > 1:
            cols = st.columns(len(pics) - 1)
            for idx, p in enumerate(pics[1:]):
                with cols[idx]:
                    st.image(p, use_container_width=True)

    # --- CONTINUT ---
    st.markdown(f"<span class='gold-text'>✨ {event.event_date} • ANUL {event.year}</span>", unsafe_allow_html=True)
    st.title(event.title)

    st.markdown(f"**Importanță:** {int(event.impact_score)}%")
    st.progress(min(event.impact_score / 100, 1.0))

    st.markdown("---")
    st.markdown(event.ai_summary)
else:
    st.info("Rulează main.py pentru a genera datele de azi!")