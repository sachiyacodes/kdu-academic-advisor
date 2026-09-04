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
    render_page_header,
    render_step_tracker,
    render_ml_prediction_card,
)
from src.academic.profile import build_academic_profile
from src.ai.recommendation_engine import generate_recommendations
from src.ai.explanations import generate_all_explanations
from src.data import database as db

st.set_page_config(page_title=f"Recommendations - {APP_TITLE}", page_icon="🎓", layout="wide")
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
            completed += [2]
        if db.get_student_interests(student["student_id"]):
            completed += [3]
    render_step_tracker(current_step=4, completed_steps=completed)

render_page_header(
    "Specialization Recommendations",
    "Ranked matches combining weighted academic scoring and content-based interest matching.",
    kicker="STEP 4 OF 6",
)

if not student:
    st.warning("Please set up your **Academic Profile** first.")
    st.stop()

student_id = student["student_id"]
student_courses = db.get_student_courses(student_id)

if not student_courses:
    render_empty_state(
        "No course history found. Add your completed courses in **Course History** "
        "to receive recommendations."
    )
    st.stop()

profile = build_academic_profile(
    student_id=student_id,
    degree=student["degree"],
    year=student["year"],
    semester=student["semester"],
    course_records=student_courses,
)

student_interests = db.get_student_interests(student_id)
selected_interest_names = [i["subject_area"] for i in student_interests]

scores = generate_recommendations(profile, selected_interest_names)
explanations = generate_all_explanations(scores)

st.markdown("## Comparison")
fig = render_specialization_comparison_chart(scores)
st.plotly_chart(fig, width="stretch")
render_weight_disclosure()

st.markdown("## Detailed Results")

for score in scores:
    with st.expander(
        f"#{score.rank} — {score.specialization_name} ({score.final_score:.1f}/100)",
        expanded=(score.rank <= 2),
    ):
        render_score_breakdown(score)

        fig = render_recommendation_breakdown_chart(score)
        st.plotly_chart(fig, width="stretch")

        st.markdown(
            f"**Evidence Level:** {render_evidence_badge(score.evidence_level)}",
            unsafe_allow_html=True,
        )
        st.caption(f"{score.relevant_course_count} relevant completed courses.")

        st.markdown("**Explanation**")
        explanation = explanations.get(score.specialization_name)
        if explanation:
            render_explanation(explanation)

from ml.predict import is_model_available, predict_specialization

if is_model_available() and profile.subject_performances:
    st.markdown("## Experimental ML Cross-Check")
    st.caption("Side-by-side comparison using our Decision Tree model trained on 750 synthetic student profiles.")

    subj_averages = {area: perf.average_mark for area, perf in profile.subject_performances.items()}
    pred_result = predict_specialization(subj_averages)
    if pred_result:
        pred_spec, probs = pred_result
        top_rule_spec = scores[0].specialization_name if scores else ""
        render_ml_prediction_card(pred_spec, probs, top_rule_spec)

st.markdown("## How This Works")
st.markdown(f"""
This recommendation combines three AI techniques:

1. **Rule-Based Reasoning** — checks prerequisites, academic stage, and eligibility
2. **Weighted Knowledge-Based Scoring** — evaluates academic fit using specialization-specific subject weights
3. **Content-Based Interest Matching** — matches your interests against specialization profiles using cosine similarity

The final score combines **Academic Fit** ({int(ACADEMIC_WEIGHT*100)}% weight) and
**Interest Alignment** ({int(INTEREST_WEIGHT*100)}% weight).
""")
render_weight_disclosure()

render_disclaimer()
