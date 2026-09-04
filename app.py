"""
AI-Based IT Specialization & Course Recommendation System
KDU - IT3182 Essentials of Artificial Intelligence - Group 22

Main application entry point and dashboard.
Run: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import APP_TITLE, APP_SUBTITLE, DISCLAIMER
from src.ui.styles import get_custom_css
from src.ui.components import (
    render_metric_card,
    render_disclaimer,
    render_empty_state,
    render_page_header,
    render_step_tracker,
)
from src.data import database as db

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

# Try to load existing student data
try:
    student = db.get_student()
except FileNotFoundError:
    st.error(
        "Database not found. Please run `python scripts/seed_database.py` first. "
        "See README.md for setup instructions."
    )
    st.stop()

student_courses = db.get_student_courses(student["student_id"]) if student else []
student_interests = db.get_student_interests(student["student_id"]) if student else []

with st.sidebar:
    st.markdown("### Recommendation System")
    st.caption(APP_SUBTITLE)
    st.markdown("---")
    completed = []
    if student:
        completed.append(1)
    if student_courses:
        completed.append(2)
    if student_interests:
        completed.append(3)
    if student_courses:
        completed += [4, 5, 6]
    render_step_tracker(current_step=0, completed_steps=completed)

render_page_header(
    APP_TITLE,
    "Academic decision support powered by rule-based reasoning, weighted knowledge-based scoring, and content-based interest matching.",
    kicker="DASHBOARD",
)

if student:
    from src.academic.profile import build_academic_profile
    from src.academic.gpa import get_gpa_classification

    profile = build_academic_profile(
        student_id=student["student_id"],
        degree=student["degree"],
        year=student["year"],
        semester=student["semester"],
        course_records=student_courses,
    )

    st.markdown("## Academic Summary")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("GPA", f"{profile.gpa:.2f}", get_gpa_classification(profile.gpa))
    with col2:
        render_metric_card("Completed Courses", str(profile.completed_course_count), "courses")
    with col3:
        render_metric_card("Credits Earned", str(profile.total_credits), "credits")
    with col4:
        render_metric_card("Academic Stage", profile.academic_stage, student["degree"])

    if profile.subject_performances:
        st.markdown("## Strongest Subject Areas")
        sorted_subjects = sorted(
            profile.subject_performances.items(),
            key=lambda x: x[1].average_mark,
            reverse=True,
        )
        cols = st.columns(min(len(sorted_subjects), 4))
        for i, (area, perf) in enumerate(sorted_subjects[:4]):
            with cols[i]:
                render_metric_card(area, f"{perf.average_mark:.1f}", f"{perf.course_count} courses")

    if student_interests:
        st.markdown("## Selected Interests")
        interest_names = [i["name"] for i in student_interests]
        st.write(", ".join(interest_names))

    if student_courses:
        st.markdown("## Top Match Preview")

        from src.ai.recommendation_engine import generate_recommendations

        selected_interest_names = [i["subject_area"] for i in student_interests] if student_interests else []
        scores = generate_recommendations(profile, selected_interest_names)

        if scores:
            top = scores[0]
            st.success(
                f"**{top.specialization_name}** — Compatibility Score {top.final_score:.1f}/100 · {top.evidence_level}"
            )
            st.caption("Open **Recommendations** in the sidebar for the full breakdown and explanation.")

else:
    render_empty_state(
        "No student data found yet. Start by setting up your academic profile "
        "using **Academic Profile** in the sidebar."
    )

    st.markdown("## How This Works")
    st.markdown("""
    1. **Academic Profile** — enter your degree, year, and semester
    2. **Course History** — add completed courses with marks
    3. **Interests** — select the subject areas you're drawn to
    4. **Recommendations** — see AI-generated specialization matches
    5. **Course Recommendations** — see which courses to take next
    6. **Analysis** — explore detailed academic analytics
    """)

render_disclaimer()
