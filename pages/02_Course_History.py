"""
Page 2: Course History

Students enter their completed courses with marks.
System auto-calculates grades, grade points, and GPA.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import APP_TITLE, CourseStatus
from src.ui.styles import get_custom_css
from src.ui.components import render_disclaimer
from src.academic.grading import mark_to_grade, format_grade_display
from src.academic.gpa import calculate_gpa, get_gpa_classification
from src.data import database as db

st.set_page_config(page_title=f"Course History - {APP_TITLE}", page_icon="📚", layout="wide")
st.markdown(get_custom_css(), unsafe_allow_html=True)

st.title("📚 Course History")
st.markdown("*Enter your completed courses to build your academic profile.*")
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

# Get available courses for this degree
available_courses = db.get_all_courses(degree=student["degree"])
existing_records = db.get_student_courses(student_id)
existing_course_ids = {r["course_id"] for r in existing_records}

# Add course form
st.subheader("Add Course Record")

# Filter to courses not yet added
courses_to_add = [c for c in available_courses if c["course_id"] not in existing_course_ids]

if courses_to_add:
    with st.form("add_course_form"):
        col1, col2 = st.columns([3, 1])

        with col1:
            course_options = {
                f"{c['course_code']} - {c['course_name']} (Y{c['year']}S{c['semester']}, {c['subject_area']})": c
                for c in courses_to_add
            }
            selected_course_key = st.selectbox(
                "Select Course",
                options=list(course_options.keys()),
            )

        with col2:
            mark = st.number_input(
                "Mark (0-100)",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=0.5,
            )

        submitted = st.form_submit_button("Add Course", use_container_width=True, type="primary")

        if submitted:
            selected_course = course_options[selected_course_key]
            grade, grade_point = mark_to_grade(mark)

            # Determine status
            status = CourseStatus.COMPLETED.value
            if mark < 40:
                status = CourseStatus.FAILED.value

            db.save_student_course(
                student_id=student_id,
                course_id=selected_course["course_id"],
                mark=mark,
                grade=grade,
                grade_point=grade_point,
                status=status,
            )
            st.success(
                f"Added: {selected_course['course_code']} - "
                f"Mark: {mark} ({grade}, GP: {grade_point})"
            )
            st.rerun()
else:
    st.info("All available courses for your degree have been added.")

# Display current course history
st.markdown("---")
st.subheader("Your Course History")

if existing_records:
    # Build display dataframe
    display_data = []
    for record in existing_records:
        display_data.append({
            "Code": record["course_code"],
            "Course": record["course_name"],
            "Year": record["year"],
            "Sem": record["semester"],
            "Subject Area": record["subject_area"],
            "Credits": record["credits"],
            "Mark": record["mark"],
            "Grade": record["grade"],
            "GP": record["grade_point"],
            "Status": record["status"].capitalize(),
        })

    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # GPA Summary
    gpa, credits_earned, credits_attempted = calculate_gpa(existing_records)
    classification = get_gpa_classification(gpa)

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("GPA", f"{gpa:.2f}")
    with col2:
        st.metric("Classification", classification)
    with col3:
        st.metric("Credits Earned", credits_earned)
    with col4:
        st.metric("Total Courses", len(existing_records))

    # Delete option
    st.markdown("---")
    st.subheader("Remove Course")
    course_to_remove = st.selectbox(
        "Select course to remove",
        options=[
            f"{r['course_code']} - {r['course_name']}" for r in existing_records
        ],
        key="remove_select",
    )
    if st.button("Remove Selected Course", type="secondary"):
        idx = [
            f"{r['course_code']} - {r['course_name']}" for r in existing_records
        ].index(course_to_remove)
        record = existing_records[idx]
        db.delete_student_course(student_id, record["course_id"])
        st.success(f"Removed: {record['course_code']}")
        st.rerun()

else:
    st.info("No courses added yet. Use the form above to add your completed courses.")

render_disclaimer()
