"""
Page 5: Course Recommendations

Uses rule-based reasoning (AI Concept 1) to categorize courses as:
- Recommended Now (prerequisites + stage satisfied)
- Recommended Later (relevant but missing prerequisites/stage)
- Low Priority (not strongly related)
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import APP_TITLE
from src.ui.styles import get_custom_css
from src.ui.components import render_disclaimer, render_empty_state
from src.academic.profile import build_academic_profile
from src.ai.recommendation_engine import generate_recommendations
from src.ai.rule_engine import get_course_recommendations
from src.data import database as db

st.set_page_config(page_title=f"Course Recommendations - {APP_TITLE}", page_icon="📖", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("📖 Course Recommendations")
st.markdown("*Rule-based course recommendations based on prerequisites, academic stage, and specialization relevance.*")
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
        "No course history found. Add courses in **Course History** first.",
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

# Get top specialization areas for relevance filtering
student_interests = db.get_student_interests(student_id)
selected_interest_names = [i["subject_area"] for i in student_interests]
scores = generate_recommendations(profile, selected_interest_names)

# Collect subject areas from top 3 specializations
top_spec_areas = set()
for score in scores[:3]:
    top_spec_areas.update(score.available_subject_areas)
    # Also add areas from the specialization weights
    from src.config.settings import SPECIALIZATION_WEIGHTS
    if score.specialization_name in SPECIALIZATION_WEIGHTS:
        top_spec_areas.update(SPECIALIZATION_WEIGHTS[score.specialization_name].keys())

# Get all courses and prerequisites
all_courses = db.get_all_courses(degree=student["degree"])
all_prerequisites = db.get_all_prerequisites()

# Generate course recommendations
recommendations = get_course_recommendations(
    profile=profile,
    all_courses=all_courses,
    all_prerequisites=all_prerequisites,
    top_specialization_areas=top_spec_areas,
    degree_filter=student["degree"],
)

# Display by category
categories = {
    "Recommended Now": "🟢",
    "Recommended Later": "🟡",
    "Low Priority": "⚪",
}

for category, icon in categories.items():
    cat_recs = [r for r in recommendations if r.category == category]

    st.subheader(f"{icon} {category} ({len(cat_recs)})")

    if cat_recs:
        data = []
        for rec in cat_recs:
            row = {
                "Code": rec.course.course_code,
                "Course": rec.course.course_name,
                "Year": rec.course.year,
                "Sem": rec.course.semester,
                "Subject Area": rec.course.subject_area,
                "Credits": rec.course.credits,
                "Reason": rec.reason,
            }
            if rec.missing_prerequisites:
                row["Missing Prerequisites"] = ", ".join(rec.missing_prerequisites)
            else:
                row["Missing Prerequisites"] = "-"
            data.append(row)

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.caption(f"No courses in this category.")

    st.markdown("---")

# Summary
st.subheader("How Course Recommendations Work")
st.markdown("""
This uses **Rule-Based Reasoning** (AI Concept 1):

```
IF prerequisites are completed
   AND academic stage is sufficient
   AND course is relevant to top specializations
THEN → Recommended Now

ELIF course is relevant but missing prerequisites/stage
THEN → Recommended Later

ELSE → Low Priority
```
""")

render_disclaimer()
