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

from src.config.settings import APP_TITLE, CourseStatus, CourseType, SUBJECT_AREA_ORDER
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
            student = db.get_current_student()
            s_year = student.get("year", 2) if student else 2
            s_sem = student.get("semester", 2) if student else 2
            load_demo_profile(demo_keys[selected_idx], year=s_year, semester=s_sem)
            st.success(f"Loaded {DEMO_PROFILES[demo_keys[selected_idx]]['title']} (autofilled prior semesters for Year {s_year} Sem {s_sem})!")
            st.rerun()
    st.info(DEMO_PROFILES[demo_keys[selected_idx]]["description"])

st.markdown("## Add a Course")

courses_to_add = [c for c in available_courses if c["course_id"] not in existing_course_ids]

if courses_to_add:
    with st.form("add_course_form"):
        col1, col2 = st.columns([3, 1])

        with col1:
            course_options = {
                f"{c['course_code']} — {c['course_name']} [{c.get('course_type', 'Core')}] (Y{c['year']}S{c['semester']}, {c['subject_area']})": c
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
    if student["degree"] == "Custom / Other University Degree":
        st.info("You are using **Custom / Other University Mode**. Add your modules using the form below.")
    else:
        st.info("All curriculum courses for your degree have been added.")

is_custom = (student["degree"] == "Custom / Other University Degree")
with st.expander("➕ Add Custom / Unlisted Course (Any University)", expanded=is_custom and len(existing_records) == 0):
    st.caption(
        "Students from any university (SLIIT, IIT, Moratuwa, Colombo, Ruhuna, etc.) or students with transfer credits "
        "can enter custom courses mapped into the 13 canonical computing subject areas."
    )
    with st.form("add_custom_course_form"):
        col_c1, col_c2 = st.columns([1, 2])
        with col_c1:
            custom_code = st.text_input("Course Code *", placeholder="e.g. CS2040", key="c_code").strip().upper()
        with col_c2:
            custom_name = st.text_input("Course Name *", placeholder="e.g. Mobile Application Development", key="c_name").strip()

        col_c3, col_c4, col_c5 = st.columns(3)
        with col_c3:
            custom_year = st.selectbox("Year", options=[1, 2, 3, 4], index=student["year"] - 1, key="c_year")
        with col_c4:
            custom_semester = st.selectbox("Semester", options=[1, 2], index=student["semester"] - 1, key="c_sem")
        with col_c5:
            custom_credits = st.number_input("Credits", min_value=1, max_value=8, value=3, step=1, key="c_credits")

        col_c6, col_c7, col_c8 = st.columns([2, 1, 1])
        with col_c6:
            custom_area = st.selectbox("Subject Area *", options=SUBJECT_AREA_ORDER, key="c_area")
        with col_c7:
            custom_type = st.selectbox("Course Type", options=[ct.value for ct in CourseType], key="c_type")
        with col_c8:
            custom_mark = st.number_input("Mark (0–100) *", min_value=0.0, max_value=100.0, value=70.0, step=0.5, key="c_mark")

        custom_submitted = st.form_submit_button("Add Custom Course", width="stretch", type="primary")

        if custom_submitted:
            if not custom_code or not custom_name:
                st.error("Please enter both Course Code and Course Name.")
            else:
                new_course_id = db.save_custom_course(
                    degree=student["degree"],
                    course_code=custom_code,
                    course_name=custom_name,
                    year=custom_year,
                    semester=custom_semester,
                    credits=int(custom_credits),
                    subject_area=custom_area,
                    course_type=custom_type,
                )
                c_grade, c_gp = mark_to_grade(custom_mark)
                c_status = (
                    CourseStatus.COMPLETED.value
                    if is_passing(custom_mark)
                    else CourseStatus.FAILED.value
                )
                db.save_student_course(
                    student_id=student_id,
                    course_id=new_course_id,
                    mark=custom_mark,
                    grade=c_grade,
                    grade_point=c_gp,
                    status=c_status,
                )
                st.success(f"Added custom course {custom_code} — {custom_name} ({custom_mark:g}, {c_grade})")
                st.rerun()

st.markdown("## Your Course History")

if existing_records:
    display_data = []
    for record in existing_records:
        display_data.append({
            "Code": record["course_code"],
            "Course": record["course_name"],
            "Type": record.get("course_type", "Core"),
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

    core_credits = sum(int(r["credits"]) for r in existing_records if r.get("course_type", "Core") == "Core" and r["status"] == "completed")
    elective_credits = sum(int(r["credits"]) for r in existing_records if r.get("course_type", "Core") == "Elective" and r["status"] == "completed")
    ngpa_credits = sum(int(r["credits"]) for r in existing_records if r.get("course_type", "Core") == "NGPA" and r["status"] == "completed")
    gpa_credits = core_credits + elective_credits

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("GPA", f"{gpa:.2f}")
    with col2:
        st.metric("Classification", classification)
    with col3:
        st.metric("GPA Credits Earned", gpa_credits, help=f"Core: {core_credits} cr | Elective: {elective_credits} cr")
    with col4:
        st.metric("NGPA Credits Earned", ngpa_credits, help="Non-GPA modules (English, Sports, Leadership, etc.)")

    st.caption(f"📊 **Credit Breakdown:** Core: **{core_credits}** cr | Elective: **{elective_credits}** cr | NGPA: **{ngpa_credits}** cr | Total Attempted: **{credits_attempted}** cr")

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
