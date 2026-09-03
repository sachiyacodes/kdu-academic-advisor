"""
AI-Based IT Specialization & Course Recommendation System
KDU - IT3182 Essentials of Artificial Intelligence - Group 22

Main application entry point and dashboard.
Run: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import APP_TITLE, APP_SUBTITLE, DISCLAIMER
from src.ui.styles import get_custom_css
from src.ui.components import render_metric_card, render_disclaimer, render_empty_state
from src.data import database as db

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("🎓 Navigation")
    st.markdown("---")
    st.markdown("""
    **Steps:**
    1. 📋 Set Academic Profile
    2. 📚 Enter Course History
    3. 💡 Select Interests
    4. 🎯 View Recommendations
    5. 📖 Course Recommendations
    6. 📊 Analysis
    """)
    st.markdown("---")
    st.caption(APP_SUBTITLE)

# Main Dashboard
st.title("🎓 " + APP_TITLE)
st.markdown("*Academic decision support powered by AI-based recommendation techniques.*")

st.markdown("---")

# Try to load existing student data
try:
    student = db.get_student()
except FileNotFoundError:
    st.error(
        "Database not found. Please run `python scripts/seed_database.py` first. "
        "See README.md for setup instructions."
    )
    st.stop()

if student:
    student_courses = db.get_student_courses(student["student_id"])
    student_interests = db.get_student_interests(student["student_id"])

    # Build profile for dashboard summary
    from src.academic.profile import build_academic_profile
    from src.academic.gpa import get_gpa_classification

    profile = build_academic_profile(
        student_id=student["student_id"],
        degree=student["degree"],
        year=student["year"],
        semester=student["semester"],
        course_records=student_courses,
    )

    # Dashboard metrics
    st.subheader("📊 Academic Summary")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("GPA", f"{profile.gpa:.2f}", get_gpa_classification(profile.gpa))
    with col2:
        render_metric_card("Completed Courses", str(profile.completed_course_count), "courses")
    with col3:
        render_metric_card("Credits Earned", str(profile.total_credits), "credits")
    with col4:
        render_metric_card("Academic Stage", profile.academic_stage, student["degree"])

    st.markdown("---")

    # Strongest subject areas
    if profile.subject_performances:
        st.subheader("📈 Strongest Subject Areas")
        sorted_subjects = sorted(
            profile.subject_performances.items(),
            key=lambda x: x[1].average_mark,
            reverse=True,
        )
        cols = st.columns(min(len(sorted_subjects), 4))
        for i, (area, perf) in enumerate(sorted_subjects[:4]):
            with cols[i]:
                color = "🟢" if perf.average_mark >= 75 else "🟡" if perf.average_mark >= 50 else "🔴"
                st.metric(
                    f"{color} {area}",
                    f"{perf.average_mark:.1f}",
                    f"{perf.course_count} courses",
                )

    # Selected interests
    if student_interests:
        st.subheader("💡 Selected Interests")
        interest_names = [i["name"] for i in student_interests]
        st.markdown(" | ".join([f"**{name}**" for name in interest_names]))

    # Quick recommendation preview
    if student_courses:
        st.markdown("---")
        st.subheader("🎯 Quick Recommendation Preview")

        from src.ai.recommendation_engine import generate_recommendations

        selected_interest_names = [i["subject_area"] for i in student_interests] if student_interests else []
        scores = generate_recommendations(profile, selected_interest_names)

        if scores:
            top = scores[0]
            st.success(
                f"**Top Match: {top.specialization_name}** "
                f"(Compatibility Score: {top.final_score:.1f}/100, "
                f"{top.evidence_level})"
            )
            st.caption("Go to **Recommendations** page for full details and explanations.")

else:
    # Empty state — no student data yet
    st.subheader("Welcome!")
    render_empty_state(
        "No student data found. Start by setting up your academic profile "
        "using the **Academic Profile** page in the sidebar.",
        icon="start",
    )

    st.markdown("### How to Use This System")
    st.markdown("""
    1. **Academic Profile** — Enter your degree, year, and semester
    2. **Course History** — Add your completed courses with marks
    3. **Interests** — Select your academic interests
    4. **Recommendations** — View AI-generated specialization recommendations
    5. **Course Recommendations** — See which courses to take next
    6. **Analysis** — Explore detailed academic analytics
    """)

# Footer
st.markdown("---")
render_disclaimer()
