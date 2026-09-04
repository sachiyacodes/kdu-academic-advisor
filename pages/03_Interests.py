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
from src.ui.components import render_disclaimer, render_page_header, render_step_tracker
from src.data import database as db

st.set_page_config(page_title=f"Interests - {APP_TITLE}", page_icon="🎓", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

try:
    student = db.get_student()
except FileNotFoundError:
    st.error("Database not found. Run `python scripts/seed_database.py` first.")
    st.stop()

with st.sidebar:
    st.markdown("### Recommendation System")
    st.markdown("---")
    completed = []
    if student:
        completed.append(1)
        if db.get_student_courses(student["student_id"]):
            completed.append(2)
    render_step_tracker(current_step=3, completed_steps=completed)

render_page_header(
    "Academic Interests",
    "Select the subject areas you're drawn to. These are compared against each "
    "specialization's interest profile using content-based matching.",
    kicker="STEP 3 OF 6",
)

if not student:
    st.warning("Please set up your **Academic Profile** first.")
    st.stop()

student_id = student["student_id"]

all_interests = db.get_all_interests()
current_interests = db.get_student_interests(student_id)
current_interest_ids = {i["interest_id"] for i in current_interests}

st.caption(
    "Select as many as apply — or none. Recommendations will fall back to "
    "academic performance alone if you skip this step."
)

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

if st.button("Save Interests", width="stretch", type="primary"):
    db.save_student_interests(student_id, selected_ids)
    st.success(f"Saved {len(selected_ids)} interest(s).")
    st.rerun()

if current_interests:
    st.markdown("## Current Selection")
    interest_names = [i["name"] for i in current_interests]
    st.write(", ".join(interest_names))
else:
    st.info(
        "No interests selected. Recommendations will be based solely on "
        "academic performance until you add some."
    )

render_disclaimer()
