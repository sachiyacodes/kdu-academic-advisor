"""
Page 5: Course Recommendations & 4-Year Graduation Roadmap

Implements:
1. Personalized Elective Advisor with Specialization Synergy Scores
2. Core Degree Pathway (Prerequisite & Stage Gating)
3. 4-Year Graduation Credit Audit (GPA & NGPA Targets) & Bottleneck Detector
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import (
    APP_TITLE,
    SPECIALIZATION_WEIGHTS,
    Specialization,
    GRADUATION_MIN_GPA_CREDITS,
    GRADUATION_MIN_NGPA_CREDITS,
)
from src.ui.styles import get_custom_css
from src.ui.components import (
    compute_completed_steps,
    render_disclaimer,
    render_empty_state,
    render_page_header,
    render_step_tracker,
)
from src.academic.profile import build_academic_profile
from src.academic.gpa import get_gpa_classification
from src.ai.recommendation_engine import generate_recommendations
from src.ai.rule_engine import get_course_recommendations
from src.data import database as db

st.set_page_config(page_title=f"Course Recommendations - {APP_TITLE}", page_icon="🎓", layout="wide")
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
        render_step_tracker(current_step=5, completed_steps=[])
    render_page_header(
        "Course Recommendations",
        "Rule-based course guidance based on prerequisites, academic stage, and relevance to your top specialization matches.",
        kicker="STEP 5 OF 6",
    )
    st.warning("Please set up your **Academic Profile** first.")
    st.stop()

student_id = student["student_id"]
student_courses = db.get_student_courses(student_id)

with st.sidebar:
    st.markdown("### Recommendation System")
    st.markdown("---")
    completed = compute_completed_steps(student, student_courses)
    render_step_tracker(current_step=5, completed_steps=completed)

render_page_header(
    "Course Recommendations",
    "Rule-based course guidance based on prerequisites, academic stage, and relevance to your top specialization matches.",
    kicker="STEP 5 OF 6",
)

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

student_interests = db.get_student_interests(student_id)
selected_interest_input = {
    i["subject_area"]: float(i.get("intensity", 3.0))
    for i in student_interests
} if student_interests else {}
scores = generate_recommendations(profile, selected_interest_input)

# Target Specialization Selector
all_spec_names = [s.value for s in Specialization]
top_spec_name = scores[0].specialization_name if scores else all_spec_names[0]
default_spec_idx = all_spec_names.index(top_spec_name) if top_spec_name in all_spec_names else 0

st.markdown("### 🎯 Career Pathway Alignment")
col_spec1, col_spec2 = st.columns([2, 2])

with col_spec1:
    target_spec = st.selectbox(
        "Select Target Specialization for Elective Alignment",
        options=all_spec_names,
        index=default_spec_idx,
        help="Specialization synergy scores and elective prioritization are calculated against this pathway.",
    )

is_custom_degree = (student["degree"] == "Custom / Other University Degree")
degree_filter = student["degree"]

with col_spec2:
    if is_custom_degree:
        curricula_mode = st.radio(
            "Elective Source",
            options=["All Computing Curricula (89 Electives)", "My Degree Courses Only"],
            horizontal=True,
            help="Universal mode allows exploring electives across all computing departments.",
        )
        if "All Computing" in curricula_mode:
            degree_filter = None
    else:
        st.info(f"Curriculum: **{student['degree']}** (Year {student['year']}, Semester {student['semester']})")

target_spec_areas = set()
if target_spec in SPECIALIZATION_WEIGHTS:
    target_spec_areas.update(SPECIALIZATION_WEIGHTS[target_spec].keys())

all_courses = db.get_all_courses(degree=degree_filter)
all_prerequisites = db.get_all_prerequisites()

recommendations = get_course_recommendations(
    profile=profile,
    all_courses=all_courses,
    all_prerequisites=all_prerequisites,
    top_specialization_areas=target_spec_areas,
    degree_filter=degree_filter,
    top_specialization_name=target_spec,
)

# Partition recommendations by course_type
elective_recs = [r for r in recommendations if r.course.course_type == "Elective"]
core_recs = [r for r in recommendations if r.course.course_type == "Core"]
ngpa_recs = [r for r in recommendations if r.course.course_type == "NGPA"]

# Tab structure
tab1, tab2, tab3 = st.tabs([
    f"🎯 Personalized Elective Advisor ({len(elective_recs)})",
    f"📋 Core Degree Pathway ({len(core_recs)})",
    "🎓 4-Year Graduation Roadmap & Credit Audit",
])

# =============================================================================
# TAB 1: PERSONALIZED ELECTIVE ADVISOR
# =============================================================================
with tab1:
    st.markdown("#### 🎯 Intelligent Elective Advisor")
    st.caption(
        f"Electives are prioritized using our **Specialization Synergy Score**, measuring how directly each module reinforces "
        f"the foundational skill weights of **{target_spec}**."
    )

    if not elective_recs:
        st.info("No electives available under the current curriculum filter.")
    else:
        cat_priority = {"Recommended Now": 0, "Recommended Later": 1, "Low Priority": 2}
        elective_recs.sort(key=lambda r: (-r.synergy_score, cat_priority.get(r.category, 3)))

        ready_electives = [r for r in elective_recs if r.category == "Recommended Now"]
        high_synergy_electives = [r for r in elective_recs if r.synergy_score >= 80.0]

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Total Electives", len(elective_recs))
        with col_m2:
            st.metric("Ready to Enroll", len(ready_electives))
        with col_m3:
            st.metric("High Synergy (≥80%)", len(high_synergy_electives))
        with col_m4:
            st.metric("Top Synergy Score", f"{elective_recs[0].synergy_score:.1f}%")

        col_f1, col_f2 = st.columns([2, 2])
        with col_f1:
            min_synergy = st.slider("Minimum Synergy Score", min_value=0, max_value=100, value=0, step=5)
        with col_f2:
            status_filter = st.selectbox(
                "Filter by Eligibility",
                options=["All Electives", "Ready to Enroll (Recommended Now)", "Upcoming / Stage Gated (Recommended Later)"],
            )

        filtered_electives = [r for r in elective_recs if r.synergy_score >= min_synergy]
        if status_filter == "Ready to Enroll (Recommended Now)":
            filtered_electives = [r for r in filtered_electives if r.category == "Recommended Now"]
        elif status_filter == "Upcoming / Stage Gated (Recommended Later)":
            filtered_electives = [r for r in filtered_electives if r.category == "Recommended Later"]

        if not filtered_electives:
            st.warning("No electives match the selected synergy and eligibility filters.")
        else:
            table_data = []
            for r in filtered_electives:
                badge = "🟢 Ready Now" if r.category == "Recommended Now" else ("⏳ Stage Gated" if r.category == "Recommended Later" else "⚪ Low Priority")
                row = {
                    "Code": r.course.course_code,
                    "Course Name": r.course.course_name,
                    "Year / Sem": f"Y{r.course.year} S{r.course.semester}",
                    "Subject Area": r.course.subject_area,
                    "Credits": r.course.credits,
                    "Synergy": f"{r.synergy_score:.1f}%",
                    "Eligibility": badge,
                    "Missing Prereqs": ", ".join(r.missing_prerequisites) if r.missing_prerequisites else "None",
                    "Strategic Advice": r.reason,
                }
                if is_custom_degree and not degree_filter:
                    row["Curriculum"] = r.course.degree
                table_data.append(row)

            df_elec = pd.DataFrame(table_data)
            st.dataframe(df_elec, width="stretch", hide_index=True)

            st.markdown(
                f"""
                <div style="background-color: #F8F9FA; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #9C7A3C; margin-top: 10px;">
                    <strong>💡 Specialization Synergy Advisory:</strong> Enrolling in electives with <strong>≥ 80% Synergy</strong> directly targets the skill areas most heavily weighted for <em>{target_spec}</em>. Electives below 50% are valuable for multidisciplinary breadth but contribute less to domain specialization.
                </div>
                """,
                unsafe_allow_html=True,
            )

# =============================================================================
# TAB 2: CORE DEGREE PATHWAY
# =============================================================================
with tab2:
    st.markdown("#### 📋 Core Degree Pathway")
    st.caption("Mandatory core modules required for your degree progression, categorized by immediate eligibility and prerequisite status.")

    if not core_recs:
        st.success(
            f"🎉 **Core Curriculum Completed!** You have completed all core requirements for **{student['degree']}**."
        )
    else:
        ready_core = [r for r in core_recs if r.category == "Recommended Now"]
        gated_core = [r for r in core_recs if r.category == "Recommended Later"]
        other_core = [r for r in core_recs if r.category not in ("Recommended Now", "Recommended Later")]

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.metric("Ready to Enroll Now", len(ready_core))
        with col_c2:
            st.metric("Upcoming / Prerequisite Gated", len(gated_core) + len(other_core))

        sub_tab1, sub_tab2 = st.tabs([
            f"🟢 Ready to Enroll Now ({len(ready_core)})",
            f"⏳ Upcoming / Gated Modules ({len(gated_core) + len(other_core)})",
        ])

        with sub_tab1:
            if not ready_core:
                st.info("No core modules are currently ready to enroll. (You may have finished this semester's core courses).")
            else:
                data_ready = []
                for r in ready_core:
                    data_ready.append({
                        "Code": r.course.course_code,
                        "Course Name": r.course.course_name,
                        "Year / Sem": f"Y{r.course.year} S{r.course.semester}",
                        "Subject Area": r.course.subject_area,
                        "Credits": r.course.credits,
                        "Unlock Power": f"Unlocks {r.chain_impact_count} future course(s)" if r.chain_impact_count > 0 else "Terminal module",
                        "Reason": r.reason,
                    })
                st.dataframe(pd.DataFrame(data_ready), width="stretch", hide_index=True)

        with sub_tab2:
            upcoming_list = gated_core + other_core
            if not upcoming_list:
                st.info("No upcoming core modules pending.")
            else:
                data_upcoming = []
                for r in upcoming_list:
                    data_upcoming.append({
                        "Code": r.course.course_code,
                        "Course Name": r.course.course_name,
                        "Year / Sem": f"Y{r.course.year} S{r.course.semester}",
                        "Subject Area": r.course.subject_area,
                        "Credits": r.course.credits,
                        "Missing Prerequisites": ", ".join(r.missing_prerequisites) if r.missing_prerequisites else "None (Academic Stage Ahead)",
                        "Status Note": r.reason,
                    })
                st.dataframe(pd.DataFrame(data_upcoming), width="stretch", hide_index=True)

# =============================================================================
# TAB 3: 4-YEAR GRADUATION ROADMAP & CREDIT AUDIT
# =============================================================================
with tab3:
    st.markdown("#### 🎓 4-Year Graduation Roadmap & Credit Audit")
    st.caption("Track your degree completion requirements against academic targets: minimum 120 GPA credits and 14 NGPA credits.")

    completed_records = [c for c in student_courses if c.get("status", "completed") == "completed"]
    completed_ids = {c["course_id"] for c in completed_records}

    completed_core_credits = sum(int(c["credits"]) for c in completed_records if c.get("course_type", "Core") == "Core")
    completed_elec_credits = sum(int(c["credits"]) for c in completed_records if c.get("course_type", "Core") == "Elective")
    completed_gpa_credits = completed_core_credits + completed_elec_credits
    completed_ngpa_credits = sum(int(c["credits"]) for c in completed_records if c.get("course_type", "Core") == "NGPA")
    total_earned = completed_gpa_credits + completed_ngpa_credits

    col_bar1, col_bar2 = st.columns(2)

    with col_bar1:
        st.markdown(f"**GPA Credits Progress: {completed_gpa_credits} / {GRADUATION_MIN_GPA_CREDITS} Credits**")
        gpa_prog = min(1.0, completed_gpa_credits / GRADUATION_MIN_GPA_CREDITS)
        st.progress(gpa_prog)
        rem_gpa = max(0, GRADUATION_MIN_GPA_CREDITS - completed_gpa_credits)
        st.caption(f"Core: **{completed_core_credits}** cr | Elective: **{completed_elec_credits}** cr | Remaining needed: **{rem_gpa}** cr")

    with col_bar2:
        st.markdown(f"**NGPA Credits Progress: {completed_ngpa_credits} / {GRADUATION_MIN_NGPA_CREDITS} Credits**")
        ngpa_prog = min(1.0, completed_ngpa_credits / GRADUATION_MIN_NGPA_CREDITS)
        st.progress(ngpa_prog)
        rem_ngpa = max(0, GRADUATION_MIN_NGPA_CREDITS - completed_ngpa_credits)
        st.caption(f"Non-GPA Modules (English, Leadership, Internship) | Remaining needed: **{rem_ngpa}** cr")

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Current Stage", f"Year {student['year']}, Sem {student['semester']}")
    with col_s2:
        st.metric("Cumulative GPA", f"{profile.gpa:.2f}")
    with col_s3:
        st.metric("GPA Classification", get_gpa_classification(profile.gpa))
    with col_s4:
        st.metric("Total Credits Earned", total_earned)

    st.markdown("---")

    all_deg_courses = db.get_all_courses(degree=student["degree"])
    deg_course_ids = {c["course_id"] for c in all_deg_courses}
    deg_course_map = {c["course_id"]: c for c in all_deg_courses}

    downstream_counts = defaultdict(int)
    for p in all_prerequisites:
        if p["course_id"] in deg_course_ids:
            prereq_id = p["prerequisite_course_id"]
            if prereq_id not in completed_ids and prereq_id in deg_course_map:
                downstream_counts[prereq_id] += 1

    bottlenecks = [
        (deg_course_map[cid], count)
        for cid, count in downstream_counts.items()
        if count >= 2
    ]
    bottlenecks.sort(key=lambda x: x[1], reverse=True)

    if bottlenecks:
        st.markdown("##### ⚠️ Critical Prerequisite Bottlenecks Detected")
        st.warning(
            "The following uncompleted courses are required prerequisites for multiple upcoming courses. "
            "Failing or delaying these courses poses a high risk of academic progression delay:"
        )
        for c, count in bottlenecks[:5]:
            st.markdown(
                f"- **{c['course_code']} — {c['course_name']}** (Year {c['year']}, Sem {c['semester']}): "
                f"Blocks **{count}** downstream courses."
            )

    st.markdown("##### 📅 4-Year Degree Schedule")
    for yr in [1, 2, 3, 4]:
        with st.expander(f"Year {yr} Modules", expanded=(yr == student["year"])):
            c_sem1, c_sem2 = st.columns(2)

            for sem, col in [(1, c_sem1), (2, c_sem2)]:
                with col:
                    st.markdown(f"**Semester {sem}**")
                    sem_courses = [c for c in all_deg_courses if c["year"] == yr and c["semester"] == sem]
                    if not sem_courses:
                        st.caption("No courses listed for this semester.")
                    else:
                        for c in sem_courses:
                            cid = c["course_id"]
                            c_type = c.get("course_type", "Core")
                            type_tag = f"[{c_type}]"
                            if cid in completed_ids:
                                rec = next((r for r in completed_records if r["course_id"] == cid), None)
                                grade_str = f"({rec['grade']})" if rec else ""
                                st.markdown(f"✅ **{c['course_code']}** {type_tag} — {c['course_name']} {grade_str}")
                            elif yr < student["year"] or (yr == student["year"] and sem <= student["semester"]):
                                st.markdown(f"⏳ **{c['course_code']}** {type_tag} — {c['course_name']} *(Pending/Retake)*")
                            else:
                                st.markdown(f"🔒 **{c['course_code']}** {type_tag} — {c['course_name']} *({c['credits']} cr)*")

st.markdown("---")
st.markdown("### How AI Course Guidance Works")
st.markdown(
    f"""
    This system combines two intelligent decision models:
    1. **Rule-Based Knowledge Engine (AI Concept 1):** Applies academic catalog rules governing prerequisites, academic stage progression, and credit eligibility.
    2. **Specialization Synergy Heuristic:** Calculates how strongly each elective's subject area matches the target specialization weight vector:
    $$\\text{{Synergy}}(e, s) = \\frac{{\\text{{Weight}}(s, \\text{{area}}(e))}}{{\\max_a \\text{{Weight}}(s, a)}} \\times 100$$
    """
)

render_disclaimer()
