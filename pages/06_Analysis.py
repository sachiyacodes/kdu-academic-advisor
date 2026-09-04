"""
Page 6: Academic Analysis

Visualizations and detailed analytics of the student's academic profile.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import APP_TITLE
from src.ui.styles import get_custom_css
from src.ui.components import (
    render_disclaimer,
    render_subject_strengths_chart,
    render_empty_state,
    render_page_header,
    render_step_tracker,
)
from src.academic.profile import build_academic_profile
from src.academic.gpa import calculate_gpa, get_gpa_classification
from src.ai.recommendation_engine import generate_recommendations
from src.data import database as db

INK = "#1A2333"
BRASS = "#9C7A3C"
GRID = "#E4E0D6"

st.set_page_config(page_title=f"Analysis - {APP_TITLE}", page_icon="🎓", layout="wide")
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
            completed += [2, 4, 5]
        if db.get_student_interests(student["student_id"]):
            completed.append(3)
    render_step_tracker(current_step=6, completed_steps=completed)

render_page_header(
    "Academic Analysis",
    "Detailed analytics across subject-area performance, mark distribution, and specialization fit.",
    kicker="STEP 6 OF 6",
)

if not student:
    st.warning("Please set up your **Academic Profile** first.")
    st.stop()

student_id = student["student_id"]
student_courses = db.get_student_courses(student_id)

if not student_courses:
    render_empty_state("No course history found. Add courses in **Course History** first.")
    st.stop()

profile = build_academic_profile(
    student_id=student_id,
    degree=student["degree"],
    year=student["year"],
    semester=student["semester"],
    course_records=student_courses,
)

st.markdown("## Performance by Subject Area")

if profile.subject_performances:
    fig = render_subject_strengths_chart(profile.subject_performances)
    if fig:
        st.plotly_chart(fig, width="stretch")

    perf_data = []
    for area, perf in sorted(
        profile.subject_performances.items(), key=lambda x: x[1].average_mark, reverse=True,
    ):
        perf_data.append({
            "Subject Area": area,
            "Average Mark": f"{perf.average_mark:.1f}",
            "Courses": perf.course_count,
            "Total Credits": perf.total_credits,
        })
    st.dataframe(pd.DataFrame(perf_data), width="stretch", hide_index=True)

st.markdown("## Mark Distribution")

marks = [float(c["mark"]) for c in student_courses if c.get("status") == "completed"]
if marks:
    fig = go.Figure(data=[go.Histogram(x=marks, nbinsx=20, marker_color=BRASS)])
    fig.update_layout(
        xaxis_title="Mark", yaxis_title="Number of Courses", height=300,
        margin=dict(l=20, r=20, t=20, b=30),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#4A5468"),
        xaxis=dict(gridcolor=GRID), yaxis=dict(gridcolor=GRID),
    )
    st.plotly_chart(fig, width="stretch")
else:
    st.caption("No completed courses with marks yet.")

st.markdown("## Specialization Fit")

student_interests = db.get_student_interests(student_id)
selected_interest_names = [i["subject_area"] for i in student_interests]
scores = generate_recommendations(profile, selected_interest_names)

if scores:
    spec_names = [s.specialization_name for s in scores]
    academic_fits = [s.academic_fit for s in scores]
    interest_scores = [s.interest_alignment for s in scores]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=academic_fits + [academic_fits[0]], theta=spec_names + [spec_names[0]],
        fill="toself", name="Academic Fit", line_color=INK,
    ))
    fig.add_trace(go.Scatterpolar(
        r=interest_scores + [interest_scores[0]], theta=spec_names + [spec_names[0]],
        fill="toself", name="Interest Alignment", line_color=BRASS, opacity=0.6,
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100], gridcolor=GRID)),
        height=450, margin=dict(l=40, r=40, t=20, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#4A5468"),
    )
    st.plotly_chart(fig, width="stretch")

    summary_data = []
    for s in scores:
        summary_data.append({
            "Rank": s.rank,
            "Specialization": s.specialization_name,
            "Academic Fit": f"{s.academic_fit:.1f}",
            "Interest": f"{s.interest_alignment:.1f}",
            "Final Score": f"{s.final_score:.1f}",
            "Evidence": s.evidence_level,
        })
    st.dataframe(pd.DataFrame(summary_data), width="stretch", hide_index=True)

st.markdown("## Academic Summary")

gpa, credits_earned, credits_attempted = calculate_gpa(student_courses)
classification = get_gpa_classification(gpa)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("GPA", f"{gpa:.2f}")
with col2:
    st.metric("Classification", classification)
with col3:
    st.metric("Credits Earned", credits_earned)
with col4:
    st.metric("Courses Completed", profile.completed_course_count)
with col5:
    st.metric("Stage", profile.academic_stage)

render_disclaimer()
