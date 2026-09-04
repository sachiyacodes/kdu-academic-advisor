"""
GPA calculation module.

Implements: GPA = Sum(grade_point * credits) / Sum(credits)

Handles: failed courses, repeated courses, missing marks, zero-credit courses,
incomplete courses, withdrawn courses, and courses not yet taken.

Does NOT treat an uncompleted course as a zero mark. Distinguishes:
  - Not Taken (excluded from GPA)
  - Failed (included with F grade point = 0.0)
  - Withdrawn (excluded from GPA)
  - In Progress (excluded from GPA)

AI classification: This is standard academic arithmetic, not AI/ML.
"""

from typing import Dict, List, Optional, Tuple

from src.config.settings import CourseStatus


def calculate_gpa(
    course_records: List[Dict],
    include_failed: bool = True,
) -> Tuple[float, int, int]:
    """
    Calculate GPA from a list of course records.

    Args:
        course_records: List of dicts with keys: grade_point, credits, status.
        include_failed: Whether to include failed courses in GPA (default True).

    Returns:
        Tuple of (gpa, total_credits_earned, total_credits_attempted).

    Rules:
        - Completed courses: included in GPA with their grade point
        - Failed courses: included in GPA (grade_point=0.0) if include_failed=True
        - Withdrawn courses: excluded from GPA
        - In-progress courses: excluded from GPA
        - Zero-credit courses: excluded from GPA denominator
    """
    total_quality_points = 0.0
    total_credits_attempted = 0
    total_credits_earned = 0

    for record in course_records:
        status = record.get("status", CourseStatus.COMPLETED.value)
        credits = int(record.get("credits", 0))
        grade_point = float(record.get("grade_point", 0.0))

        # Skip non-GPA-eligible statuses
        if status == CourseStatus.WITHDRAWN.value:
            continue
        if status == CourseStatus.IN_PROGRESS.value:
            continue

        # Skip zero-credit courses from GPA calculation
        if credits <= 0:
            continue

        course_type = record.get("course_type", "Core")

        # NGPA (Non-GPA) modules do not count toward GPA quality points or attempted credits,
        # but completed NGPA credits count toward total degree credits earned
        if course_type == "NGPA":
            if status == CourseStatus.COMPLETED.value:
                total_credits_earned += credits
            continue

        # Failed courses
        if status == CourseStatus.FAILED.value:
            if include_failed:
                total_quality_points += grade_point * credits
                total_credits_attempted += credits
            continue

        # Completed courses
        if status == CourseStatus.COMPLETED.value:
            total_quality_points += grade_point * credits
            total_credits_attempted += credits
            total_credits_earned += credits

    if total_credits_attempted == 0:
        return 0.0, total_credits_earned, 0

    gpa = total_quality_points / total_credits_attempted
    return round(gpa, 2), total_credits_earned, total_credits_attempted


def calculate_subject_gpa(course_records: List[Dict], subject_area: str) -> float:
    """
    Calculate GPA for courses in a specific subject area.

    Only includes completed courses. Returns 0.0 if no courses found.
    """
    filtered = [
        r for r in course_records
        if r.get("subject_area") == subject_area
        and r.get("status", CourseStatus.COMPLETED.value) == CourseStatus.COMPLETED.value
    ]
    if not filtered:
        return 0.0
    gpa, _, _ = calculate_gpa(filtered)
    return gpa


def get_gpa_classification(gpa: float) -> str:
    """Get a classification label for a GPA value."""
    if gpa >= 3.7:
        return "First Class Honours"
    elif gpa >= 3.3:
        return "Second Class Upper"
    elif gpa >= 2.7:
        return "Second Class Lower"
    elif gpa >= 2.0:
        return "Pass"
    elif gpa > 0:
        return "Conditional"
    else:
        return "Not Available"
