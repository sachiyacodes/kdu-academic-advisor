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
    compute_completed_steps,
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

if not student:
    with st.sidebar:
        st.markdown("### Recommendation System")
        st.markdown("---")
        render_step_tracker(current_step=4, completed_steps=[])
    render_page_header(
        "Specialization Recommendations",
        "Ranked matches combining weighted academic scoring and content-based interest matching.",
        kicker="STEP 4 OF 6",
    )
    st.warning("Please set up your **Academic Profile** first.")
    st.stop()

student_id = student["student_id"]
student_courses = db.get_student_courses(student_id)

with st.sidebar:
    st.markdown("### Recommendation System")
    st.markdown("---")
    completed = compute_completed_steps(student, student_courses)
    render_step_tracker(current_step=4, completed_steps=completed)

render_page_header(
    "Specialization Recommendations",
    "Ranked matches combining weighted academic scoring and content-based interest matching.",
    kicker="STEP 4 OF 6",
)

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
# Support continuous intensity mapping if available
selected_interests_input = {
    i["subject_area"]: float(i.get("intensity", 3.0))
    for i in student_interests
}

scores = generate_recommendations(profile, selected_interests_input)
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

        col_ev1, col_ev2 = st.columns([1, 1])
        with col_ev1:
            st.markdown(
                f"**Evidence Level:** {render_evidence_badge(score.evidence_level)}",
                unsafe_allow_html=True,
            )
            st.caption(f"{score.relevant_course_count} relevant completed courses.")
        with col_ev2:
            if score.evidence_level != "Strong Evidence":
                st.caption(f"ℹ️ **Evidence-Calibrated Fit:** {score.calibrated_fit:.1f}/100 (Adjusted for transcript sample size)")

        st.markdown("**Explanation**")
        explanation = explanations.get(score.specialization_name)
        if explanation:
            render_explanation(explanation)
            if explanation.counterfactuals:
                st.markdown("---")
                st.markdown("**Actionable Progression Advice**")
                for cf in explanation.counterfactuals:
                    st.info(cf)

from ml.predict import is_model_available, predict_with_consensus

if is_model_available() and profile.subject_performances:
    st.markdown("## Machine Learning Cross-Check & Consensus")
    st.caption("Side-by-side empirical benchmark using Random Forest and Decision Tree models trained with 5-Fold Cross-Validation.")

    subj_averages = {area: perf.average_mark for area, perf in profile.subject_performances.items()}
    consensus_info = predict_with_consensus(subj_averages)
    if consensus_info:
        top_rule_spec = scores[0].specialization_name if scores else ""
        render_ml_prediction_card(
            prediction=consensus_info["prediction"],
            probabilities=consensus_info["probabilities"],
            top_rule_spec=top_rule_spec,
            consensus_info=consensus_info,
        )

# Human-in-the-Loop Recommendation Feedback
st.markdown("## Recommendation Feedback")
st.caption("Help us improve the recommendation engine by providing feedback on your results.")
with st.container():
    top_spec_name = scores[0].specialization_name if scores else "General"
    fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 3])
    with fb_col1:
        if st.button("👍 Helpful", key="fb_thumbs_up", width="stretch"):
            db.save_student_feedback(student_id, top_spec_name, 1, "Helpful recommendation")
            st.session_state[f"fb_{student_id}_{top_spec_name}"] = "positive"
            st.success("Thank you for your feedback!")
    with fb_col2:
        if st.button("👎 Needs Tuning", key="fb_thumbs_down", width="stretch"):
            db.save_student_feedback(student_id, top_spec_name, -1, "Needs tuning")
            st.session_state[f"fb_{student_id}_{top_spec_name}"] = "tuning"
            st.info("Thank you! Your feedback helps calibrate future recommendations.")
    with fb_col3:
        if st.session_state.get(f"fb_{student_id}_{top_spec_name}"):
            st.caption(f"✓ Feedback recorded for **{top_spec_name}**.")

st.markdown("## How This Works")
st.markdown(f"""
This recommendation combines three AI techniques:

1. **Rule-Based Reasoning** — checks prerequisites, academic stage, and course eligibility
2. **Weighted Knowledge-Based Scoring** — evaluates academic fit using specialization-specific subject weights with missing-data renormalization
3. **Content-Based Interest Matching** — matches your interests with continuous intensity scaling against specialization profiles using cosine similarity

The final score combines **Academic Fit** ({int(ACADEMIC_WEIGHT*100)}% weight) and
**Interest Alignment** ({int(INTEREST_WEIGHT*100)}% weight).
""")
render_weight_disclosure()

render_disclaimer()
