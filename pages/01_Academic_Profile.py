"""
Page 1: Academic Profile Setup

Students enter their degree, year, and semester.
System auto-detects academic stage from this information.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import APP_TITLE, DEGREE_PROGRAMS
from src.ui.styles import get_custom_css
from src.ui.components import render_disclaimer
from src.data import database as db

st.set_page_config(page_title=f"Academic Profile - {APP_TITLE}", page_icon="📋", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("📋 Academic Profile")
st.markdown("*Set up your academic profile to receive personalized recommendations.*")
st.markdown("---")

# Load existing student data
try:
    student = db.get_student()
except FileNotFoundError:
    st.error("Database not found. Run `python scripts/seed_database.py` first.")
    st.stop()

# Pre-fill from existing data
default_degree = student["degree"] if student else DEGREE_PROGRAMS[0]
default_year = student["year"] if student else 1
default_semester = student["semester"] if student else 1

with st.form("academic_profile_form"):
    st.subheader("Your Academic Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        degree = st.selectbox(
            "Degree Program",
            options=DEGREE_PROGRAMS,
            index=DEGREE_PROGRAMS.index(default_degree) if default_degree in DEGREE_PROGRAMS else 0,
            help="Select your current degree program.",
        )

    with col2:
        year = st.selectbox(
            "Current Year",
            options=[1, 2, 3, 4],
            index=default_year - 1,
            help="Your current academic year.",
        )

    with col3:
        semester = st.selectbox(
            "Current Semester",
            options=[1, 2],
            index=default_semester - 1,
            help="Your current semester.",
        )

    submitted = st.form_submit_button("Save Profile", use_container_width=True, type="primary")

    if submitted:
        student_id = db.save_student(degree, year, semester)
        st.success(f"Profile saved! Student ID: {student_id}")
        st.rerun()

# Show current profile
if student:
    st.markdown("---")
    st.subheader("Current Profile")

    from src.academic.profile import detect_academic_stage

    # Calculate stage
    student_courses = db.get_student_courses(student["student_id"])
    completed_credits = sum(
        int(c["credits"]) for c in student_courses
        if c.get("status", "completed") == "completed"
    )
    stage = detect_academic_stage(student["year"], student["semester"], completed_credits)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Degree", student["degree"])
    with col2:
        st.metric("Year", student["year"])
    with col3:
        st.metric("Semester", student["semester"])
    with col4:
        st.metric("Academic Stage", stage)

    st.markdown("---")

    # Reset option
    if st.button("Reset All Data", type="secondary"):
        db.clear_student_data()
        st.success("All student data cleared.")
        st.rerun()

render_disclaimer()
