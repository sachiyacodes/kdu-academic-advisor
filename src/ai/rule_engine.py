"""
Rule-Based Reasoning Engine — AI Concept 1.

Implements explicit rules for:
- Prerequisite satisfaction checking
- Academic stage eligibility
- Course eligibility determination
- Course recommendation categorization (Recommended Now / Later / Low Priority)

This is genuine rule-based AI: a knowledge base of academic rules applied to
student profiles to derive actionable conclusions (eligibility, recommendations).

It is NOT machine learning and must not be labeled as such (§43).
"""

from typing import Dict, List, Optional, Set, Tuple

from src.config.settings import CourseStatus, MINIMUM_PASS_MARK, SPECIALIZATION_WEIGHTS
from src.models.schemas import (
    AcademicProfile,
    Course,
    CourseRecommendation,
    StudentCourse,
)


def calculate_elective_synergy(
    subject_area: str,
    target_specialization: Optional[str] = None,
) -> float:
    """
    Calculate Specialization Synergy Score for an elective course.

    Formula:
        Synergy(e, s) = (Weight(s, area(e)) / max_a Weight(s, a)) * 100

    Returns:
        float between 0.0 and 100.0 (rounded to 1 decimal place).
    """
    if not target_specialization or target_specialization not in SPECIALIZATION_WEIGHTS:
        return 0.0

    spec_weights = SPECIALIZATION_WEIGHTS[target_specialization]
    if not spec_weights:
        return 0.0

    max_w = max(spec_weights.values()) if spec_weights else 1.0
    w = spec_weights.get(subject_area, 0.0)

    if max_w <= 0:
        return 0.0

    return round((w / max_w) * 100.0, 1)


def check_prerequisites(
    course_id: int,
    completed_course_ids: Set[int],
    all_prerequisites: List[Dict],
) -> Tuple[bool, List[Dict]]:
    """
    Check if all prerequisites for a course are satisfied.

    Args:
        course_id: The course to check prerequisites for.
        completed_course_ids: Set of course IDs the student has completed.
        all_prerequisites: List of prerequisite relationship dicts.

    Returns:
        Tuple of (all_satisfied: bool, missing_prerequisites: list of dicts).

    Rule:
        IF all prerequisite courses are in the completed set
        THEN prerequisites are satisfied
        ELSE return the list of missing prerequisites
    """
    # Find prerequisites for this course
    prereqs = [
        p for p in all_prerequisites
        if p["course_id"] == course_id
    ]

    if not prereqs:
        return True, []

    missing = []
    for prereq in prereqs:
        prereq_course_id = prereq["prerequisite_course_id"]
        if prereq_course_id not in completed_course_ids:
            missing.append(prereq)

    return len(missing) == 0, missing


def check_stage_eligibility(
    course_year: int,
    course_semester: int,
    student_year: int,
    student_semester: int,
) -> bool:
    """
    Check if the student's academic stage is sufficient for a course.

    Rule:
        IF student_year > course_year THEN eligible
        IF student_year == course_year AND student_semester >= course_semester THEN eligible
        ELSE not eligible
    """
    if student_year > course_year:
        return True
    if student_year == course_year and student_semester >= course_semester:
        return True
    return False


def categorize_course(
    course: Dict,
    profile: AcademicProfile,
    all_prerequisites: List[Dict],
    specialization_subject_areas: Set[str],
    top_specialization_name: Optional[str] = None,
) -> CourseRecommendation:
    """
    Categorize a course for recommendation using rule-based reasoning.

    Categories:
        - "Recommended Now": prerequisites + stage satisfied, relevant to specialization
        - "Recommended Later": relevant but missing prerequisites or stage
        - "Low Priority": not strongly related to student's target specializations

    Rules applied:
        1. IF course already completed THEN skip
        2. IF course subject area is relevant to specialization THEN potentially recommend
        3. IF prerequisites satisfied AND stage eligible THEN "Recommended Now"
        4. IF prerequisites NOT satisfied OR stage NOT eligible THEN "Recommended Later"
        5. ELSE "Low Priority"
    """
    course_id = course["course_id"]
    course_obj = Course(
        course_id=course_id,
        course_code=course["course_code"],
        course_name=course["course_name"],
        degree=course.get("degree", ""),
        year=int(course.get("year", 1)),
        semester=int(course.get("semester", 1)),
        credits=int(course.get("credits", 0)),
        subject_area=course.get("subject_area", ""),
        course_type=course.get("course_type", "Core"),
    )

    synergy = calculate_elective_synergy(course_obj.subject_area, top_specialization_name)

    # Get completed course IDs
    completed_ids = {c.course_id for c in profile.completed_courses}

    # Rule 1: Already completed — skip
    if course_id in completed_ids:
        return CourseRecommendation(
            course=course_obj,
            category="Completed",
            reason="You have already completed this course.",
            prerequisite_status="not_applicable",
            synergy_score=synergy,
            target_specialization=top_specialization_name or "",
        )

    # Check relevance to specialization areas
    is_relevant = course_obj.subject_area in specialization_subject_areas

    # Rule: Check prerequisites
    prereqs_satisfied, missing_prereqs = check_prerequisites(
        course_id, completed_ids, all_prerequisites
    )

    # Rule: Check stage eligibility
    stage_eligible = check_stage_eligibility(
        course_obj.year, course_obj.semester,
        profile.year, profile.semester,
    )

    # Format missing prerequisite names
    missing_names = [
        str(p.get("prereq_name") or p.get("prereq_code") or f"Course {p.get('prerequisite_course_id', '')}")
        for p in missing_prereqs
    ]

    # Chain impact: how many future courses require this course as prerequisite
    chain_impact = len([
        p for p in all_prerequisites
        if p.get("prerequisite_course_id") == course_id
    ])

    # Rule 3: Relevant, prerequisites satisfied, stage eligible
    if is_relevant and prereqs_satisfied and stage_eligible:
        if course_obj.course_type == "Elective" and top_specialization_name:
            reason_text = (
                f"Elective with {synergy}% synergy to {top_specialization_name} "
                f"in {course_obj.subject_area}. Prerequisites satisfied and stage eligible."
            )
        else:
            reason_text = (
                f"This {course_obj.subject_area} course is relevant to your "
                f"target specialization. All prerequisites are satisfied and "
                f"you are at the appropriate academic stage."
            )
        if chain_impact > 0:
            reason_text += f" (Foundational: unlocks {chain_impact} advanced course{'s' if chain_impact > 1 else ''})."

        return CourseRecommendation(
            course=course_obj,
            category="Recommended Now",
            reason=reason_text,
            prerequisite_status="satisfied",
            chain_impact_count=chain_impact,
            synergy_score=synergy,
            target_specialization=top_specialization_name or "",
        )

    # Rule 4: Relevant but missing prerequisites or stage
    if is_relevant and (not prereqs_satisfied or not stage_eligible):
        reasons = []
        if not prereqs_satisfied:
            reasons.append(f"Missing prerequisites: {', '.join(missing_names)}")
        if not stage_eligible:
            reasons.append(
                f"Course is for Year {course_obj.year} Semester {course_obj.semester}, "
                f"but you are currently in Year {profile.year} Semester {profile.semester}"
            )

        if course_obj.course_type == "Elective" and top_specialization_name:
            reason_text = f"Elective with {synergy}% synergy to {top_specialization_name}, but: {'; '.join(reasons)}."
        else:
            reason_text = f"This course is relevant to your interests but: {'; '.join(reasons)}."

        return CourseRecommendation(
            course=course_obj,
            category="Recommended Later",
            reason=reason_text,
            missing_prerequisites=missing_names,
            prerequisite_status="not_satisfied" if not prereqs_satisfied else "satisfied",
            chain_impact_count=chain_impact,
            synergy_score=synergy,
            target_specialization=top_specialization_name or "",
        )

    # Rule 5: Not directly relevant but prerequisites ok
    if not is_relevant and prereqs_satisfied and stage_eligible:
        if course_obj.course_type == "Elective" and top_specialization_name:
            reason_text = (
                f"Elective in {course_obj.subject_area} ({synergy}% synergy with {top_specialization_name}) "
                f"— may broaden your skills."
            )
        else:
            reason_text = (
                f"This {course_obj.subject_area} course is not directly related "
                f"to your top specializations but may broaden your skills."
            )
        return CourseRecommendation(
            course=course_obj,
            category="Low Priority",
            reason=reason_text,
            prerequisite_status="satisfied",
            chain_impact_count=chain_impact,
            synergy_score=synergy,
            target_specialization=top_specialization_name or "",
        )

    # Not relevant and not eligible
    if course_obj.course_type == "Elective" and top_specialization_name:
        reason_text = (
            f"Elective in {course_obj.subject_area} ({synergy}% synergy with {top_specialization_name}) "
            f"with unmet requirements."
        )
    else:
        reason_text = (
            f"This course is not directly related to your target specializations "
            f"and has unmet requirements."
        )

    return CourseRecommendation(
        course=course_obj,
        category="Low Priority",
        reason=reason_text,
        missing_prerequisites=missing_names,
        prerequisite_status="not_satisfied" if not prereqs_satisfied else "satisfied",
        chain_impact_count=chain_impact,
        synergy_score=synergy,
        target_specialization=top_specialization_name or "",
    )


def get_course_recommendations(
    profile: AcademicProfile,
    all_courses: List[Dict],
    all_prerequisites: List[Dict],
    top_specialization_areas: Set[str],
    degree_filter: Optional[str] = None,
    top_specialization_name: Optional[str] = None,
) -> List[CourseRecommendation]:
    """
    Generate course recommendations for a student.

    Applies rule-based reasoning to categorize all available courses
    into Recommended Now / Recommended Later / Low Priority.

    Args:
        profile: Student's academic profile.
        all_courses: All available courses.
        all_prerequisites: All prerequisite relationships.
        top_specialization_areas: Subject areas relevant to top-ranked specializations.
        degree_filter: Optional degree to filter courses by.
        top_specialization_name: Optional name of the top-ranked specialization to compute synergy.

    Returns:
        List of CourseRecommendation objects, sorted by category priority.
    """
    # Filter by degree if specified
    courses = all_courses
    if degree_filter:
        courses = [c for c in courses if c["degree"] == degree_filter]

    recommendations = []
    for course in courses:
        rec = categorize_course(
            course,
            profile,
            all_prerequisites,
            top_specialization_areas,
            top_specialization_name=top_specialization_name,
        )
        # Skip already-completed courses from the recommendation list
        if rec.category != "Completed":
            recommendations.append(rec)

    # Sort: Recommended Now first, then Later, then Low Priority
    category_order = {"Recommended Now": 0, "Recommended Later": 1, "Low Priority": 2}
    recommendations.sort(key=lambda r: category_order.get(r.category, 3))

    return recommendations
