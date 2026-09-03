"""
Page 4: Specialization Recommendations

The core output page — runs the full recommendation pipeline and displays
ranked specializations with score breakdowns, explanations, and visualizations.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import APP_TITLE, ACADEMIC_WEIGHT, INTEREST_WEIGHT
from src.ui.styles import get_custom_css
from src.ui.components import (
    render_disclaimer,
    render_weight_disclosure,
    render_score_breakdown,
    render_specialization_comparison_chart,
    render_recommendation_breakdown_chart,
    render_explanation,
    render_evidence_badge,
    render_empty_state,
)
from src.academic.profile import build_academic_profile
from src.ai.recommendation_engine import generate_recommendations
from src.ai.explanations import generate_all_explanations
from src.data import database as db

st.set_page_config(page_title=f"Recommendations - {APP_TITLE}", page_icon="🎯", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("🎯 Specialization Recommendations")
st.markdown("*AI-powered specialization matching based on your academic profile and interests.*")
st.markdown("---")

# Check prerequisites
try:
    student = db.get_student()
except FileNotFoundError:
    st.error("Database not found. Run `python scripts/seed_database.py` first.")
    st.stop()

if not student:
    st.warning("Please set up your **Academic Profile** first.")
    st.stop()

student_id = student["student_id"]
student_courses = db.get_student_courses(student_id)

if not student_courses:
    render_empty_state(
        "No course history found. Please add your completed courses in the "
        "**Course History** page to receive recommendations.",
        icon="data",
    )
    st.stop()

# Build profile
profile = build_academic_profile(
    student_id=student_id,
    degree=student["degree"],
    year=student["year"],
    semester=student["semester"],
    course_records=student_courses,
)

# Get interests
student_interests = db.get_student_interests(student_id)
selected_interest_names = [i["subject_area"] for i in student_interests]

# Run recommendation pipeline
scores = generate_recommendations(profile, selected_interest_names)
explanations = generate_all_explanations(scores)

# Comparison chart
st.subheader("Specialization Comparison")
fig = render_specialization_comparison_chart(scores)
st.plotly_chart(fig, use_container_width=True)
render_weight_disclosure()

st.markdown("---")

# Detailed results
st.subheader("Detailed Recommendations")

for score in scores:
    with st.expander(
        f"#{score.rank} — {score.specialization_name} "
        f"(Score: {score.final_score:.1f}/100)",
        expanded=(score.rank <= 2),
    ):
        # Score breakdown
        render_score_breakdown(score)

        st.markdown("---")

        # Breakdown chart
        fig = render_recommendation_breakdown_chart(score)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Evidence level
        st.markdown(
            f"**Evidence Level:** {render_evidence_badge(score.evidence_level)}",
            unsafe_allow_html=True,
        )
        st.caption(f"{score.relevant_course_count} relevant completed courses.")

        st.markdown("---")

        # Full explanation
        st.subheader("Explanation")
        explanation = explanations.get(score.specialization_name)
        if explanation:
            render_explanation(explanation)

# AI Methodology disclosure
st.markdown("---")
st.subheader("How This Works")
st.markdown(f"""
This recommendation uses three AI techniques:

1. **Rule-Based Reasoning** — Checks prerequisites, academic stage, and eligibility
2. **Weighted Knowledge-Based Scoring** — Evaluates academic fit using specialization-specific subject weights
3. **Content-Based Interest Matching** — Matches your interests against specialization profiles using cosine similarity

The final score combines:
- **Academic Fit** ({int(ACADEMIC_WEIGHT*100)}% weight)
- **Interest Alignment** ({int(INTEREST_WEIGHT*100)}% weight)
""")
render_weight_disclosure()

render_disclaimer()
