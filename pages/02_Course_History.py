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
from src.ui.components import (
    compute_completed_steps,
    render_disclaimer,
    render_page_header,
    render_step_tracker,
)
from src.academic.grading import is_passing, mark_to_grade
from src.academic.gpa import calculate_gpa, get_gpa_classification
from src.data import database as db

st.set_page_config(page_title=f"Course History - {APP_TITLE}", page_icon="🎓", layout="wide")
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
        render_step_tracker(current_step=2, completed_steps=[])
    render_page_header(
        "Course History",
        "Add your completed courses with marks. GPA, grades, and subject-area strengths are calculated automatically.",
        kicker="STEP 2 OF 6",
    )
    st.warning("Please set up your **Academic Profile** first.")
    st.stop()

student_id = student["student_id"]
available_courses = db.get_all_courses(degree=student["degree"])
existing_records = db.get_student_courses(student_id)
existing_course_ids = {r["course_id"] for r in existing_records}

with st.sidebar:
    st.markdown("### Recommendation System")
    st.markdown("---")
    completed = compute_completed_steps(student, existing_records)
    render_step_tracker(current_step=2, completed_steps=completed)

render_page_header(
    "Course History",
    "Add your completed courses with marks. GPA, grades, and subject-area strengths are calculated automatically.",
    kicker="STEP 2 OF 6",
)

with st.expander("⚡ Fast-Track Demo: Load Sample Student Profile", expanded=False):
    st.caption("Quickly populate a pre-configured student archetype from our test benchmark for rapid presentation and live evaluation.")
    from src.data.demo_profiles import DEMO_PROFILES, load_demo_profile
    demo_keys = list(DEMO_PROFILES.keys())
    demo_labels = [DEMO_PROFILES[k]["title"] for k in demo_keys]

    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        selected_idx = st.selectbox("Select Archetype", range(len(demo_keys)), format_func=lambda i: demo_labels[i])
    with col_d2:
        st.write("")
        st.write("")
        if st.button("Load Profile", type="primary", use_container_width=True):
            load_demo_profile(demo_keys[selected_idx])
            st.success(f"Loaded {DEMO_PROFILES[demo_keys[selected_idx]]['title']}!")
            st.rerun()
    st.info(DEMO_PROFILES[demo_keys[selected_idx]]["description"])

st.markdown("## Add a Course")

courses_to_add = [c for c in available_courses if c["course_id"] not in existing_course_ids]

if courses_to_add:
    with st.form("add_course_form"):
        col1, col2 = st.columns([3, 1])

        with col1:
            course_options = {
                f"{c['course_code']} — {c['course_name']} (Y{c['year']}S{c['semester']}, {c['subject_area']})": c
                for c in courses_to_add
            }
            selected_course_key = st.selectbox("Course", options=list(course_options.keys()))

        with col2:
            mark = st.number_input("Mark (0–100)", min_value=0.0, max_value=100.0, value=70.0, step=0.5)

        submitted = st.form_submit_button("Add Course", width="stretch", type="primary")

        if submitted:
            selected_course = course_options[selected_course_key]
            grade, grade_point = mark_to_grade(mark)

            status = (
                CourseStatus.COMPLETED.value
                if is_passing(mark)
                else CourseStatus.FAILED.value
            )

            db.save_student_course(
                student_id=student_id,
                course_id=selected_course["course_id"],
                mark=mark,
                grade=grade,
                grade_point=grade_point,
                status=status,
            )
            st.success(f"Added {selected_course['course_code']} — {mark:g} ({grade}, GP {grade_point})")
            st.rerun()
else:
    st.info("All available courses for your degree have been added.")

st.markdown("## Your Course History")

if existing_records:
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
    st.dataframe(df, width="stretch", hide_index=True)

    gpa, credits_earned, credits_attempted = calculate_gpa(existing_records)
    classification = get_gpa_classification(gpa)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("GPA", f"{gpa:.2f}")
    with col2:
        st.metric("Classification", classification)
    with col3:
        st.metric("Credits Earned", credits_earned)
    with col4:
        st.metric("Total Courses", len(existing_records))

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        with st.expander("✏️ Edit / Retake a Course"):
            edit_options = {
                f"{r['course_code']} — {r['course_name']} (Current: {r['mark']:g}, {r['grade']})": r
                for r in existing_records
            }
            edit_key = st.selectbox(
                "Select course to update mark",
                options=list(edit_options.keys()),
                key="edit_select",
            )
            if edit_key:
                rec_to_edit = edit_options[edit_key]
                new_mark = st.number_input(
                    "New Mark (0–100)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(rec_to_edit["mark"]),
                    step=0.5,
                    key="edit_mark_input",
                )
                if st.button("Update Mark", type="primary", key="btn_update_mark"):
                    new_grade, new_gp = mark_to_grade(new_mark)
                    new_status = (
                        CourseStatus.COMPLETED.value
                        if is_passing(new_mark)
                        else CourseStatus.FAILED.value
                    )
                    db.save_student_course(
                        student_id=student_id,
                        course_id=rec_to_edit["course_id"],
                        mark=new_mark,
                        grade=new_grade,
                        grade_point=new_gp,
                        status=new_status,
                    )
                    st.success(f"Updated {rec_to_edit['course_code']} to {new_mark:g} ({new_grade}, GP {new_gp})")
                    st.rerun()

    with col_m2:
        with st.expander("🗑️ Remove a Course"):
            remove_options = {
                f"{r['course_code']} — {r['course_name']}": r
                for r in existing_records
            }
            remove_key = st.selectbox(
                "Select course to remove",
                options=list(remove_options.keys()),
                key="remove_select",
            )
            if st.button("Remove Selected Course", type="secondary", key="btn_remove_course"):
                if remove_key and remove_key in remove_options:
                    rec = remove_options[remove_key]
                    db.delete_student_course(student_id, rec["course_id"])
                    st.success(f"Removed {rec['course_code']}")
                    st.rerun()

else:
    st.info("No courses added yet. Use the form above to add your completed courses.")

render_disclaimer()
