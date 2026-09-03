"""
Page 3: Interest Selection

Multi-select UI mapped 1:1 onto the canonical subject-area taxonomy (section 21).
Interests are used for Content-Based Interest Matching (AI Concept 3, FIX-3).
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import APP_TITLE
from src.ui.styles import get_custom_css
from src.ui.components import render_disclaimer
from src.data import database as db

st.set_page_config(page_title=f"Interests - {APP_TITLE}", page_icon="💡", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("💡 Academic Interests")
st.markdown("*Select the subject areas you are most interested in. These are used for interest-based matching.*")
st.markdown("---")

# Check student exists
try:
    student = db.get_student()
except FileNotFoundError:
    st.error("Database not found. Run `python scripts/seed_database.py` first.")
    st.stop()

if not student:
    st.warning("Please set up your **Academic Profile** first.")
    st.stop()

student_id = student["student_id"]

# Get all available interests (mapped 1:1 to subject areas)
all_interests = db.get_all_interests()
current_interests = db.get_student_interests(student_id)
current_interest_ids = {i["interest_id"] for i in current_interests}

st.subheader("What areas are you interested in?")
st.caption(
    "Select one or more subject areas that interest you. "
    "These will be used alongside your academic performance to generate "
    "personalized specialization recommendations. You don't have to select any."
)

# Multi-select using checkboxes for clearer UX
selected_ids = []
cols = st.columns(3)

for i, interest in enumerate(all_interests):
    col = cols[i % 3]
    with col:
        checked = st.checkbox(
            interest["name"],
            value=interest["interest_id"] in current_interest_ids,
            key=f"interest_{interest['interest_id']}",
        )
        if checked:
            selected_ids.append(interest["interest_id"])

st.markdown("---")

if st.button("Save Interests", use_container_width=True, type="primary"):
    db.save_student_interests(student_id, selected_ids)
    st.success(f"Saved {len(selected_ids)} interest(s)!")
    st.rerun()

# Show current selection summary
if current_interests:
    st.markdown("---")
    st.subheader("Current Selection")
    interest_names = [i["name"] for i in current_interests]
    st.markdown(" | ".join([f"**{name}**" for name in interest_names]))
    st.caption(f"{len(current_interests)} interest(s) selected.")
else:
    st.info(
        "No interests selected. Recommendations will be based solely on "
        "academic performance. You can always come back and add interests later."
    )

render_disclaimer()
