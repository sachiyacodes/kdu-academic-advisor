"""
Academic profile construction module.

Builds a complete AcademicProfile from student course records:
- Subject-area performance aggregation
- Academic stage detection
- Completed credits and course counts

AI classification: This is data preparation, not AI/ML.
"""

from collections import defaultdict
from typing import Dict, List, Optional

from src.academic.gpa import calculate_gpa
from src.academic.grading import mark_to_grade
from src.config.settings import (
    ACADEMIC_STAGE_THRESHOLDS,
    CourseStatus,
    SubjectArea,
)
from src.models.schemas import AcademicProfile, StudentCourse, SubjectPerformance


def build_student_courses(course_records: List[Dict]) -> List[StudentCourse]:
    """Convert raw database records to StudentCourse objects."""
    student_courses = []
    for record in course_records:
        sc = StudentCourse(
            student_id=record.get("student_id", 0),
            course_id=record.get("course_id", 0),
            course_code=record.get("course_code", ""),
            course_name=record.get("course_name", ""),
            credits=int(record.get("credits", 0)),
            subject_area=record.get("subject_area", ""),
            mark=float(record.get("mark", 0)),
            grade=record.get("grade", ""),
            grade_point=float(record.get("grade_point", 0)),
            status=record.get("status", CourseStatus.COMPLETED.value),
        )
        student_courses.append(sc)
    return student_courses


def aggregate_subject_performance(
    courses: List[StudentCourse],
) -> Dict[str, SubjectPerformance]:
    """
    Aggregate performance by subject area.

    Only includes completed courses. Calculates average mark per subject area.
    A missing subject area is NOT included — it will NOT receive a zero score (§16).
    """
    subject_data: Dict[str, List[StudentCourse]] = defaultdict(list)

    for course in courses:
        if course.status != CourseStatus.COMPLETED.value:
            continue
        subject_data[course.subject_area].append(course)

    performances = {}
    for subject_area, area_courses in subject_data.items():
        total_mark = sum(c.mark for c in area_courses)
        total_credits = sum(c.credits for c in area_courses)
        count = len(area_courses)
        avg_mark = total_mark / count if count > 0 else 0.0

        performances[subject_area] = SubjectPerformance(
            subject_area=subject_area,
            average_mark=round(avg_mark, 2),
            course_count=count,
            total_credits=total_credits,
            courses=area_courses,
        )

    return performances


def detect_academic_stage(
    year: int, semester: int, completed_credits: int
) -> str:
    """
    Detect academic stage based on year, semester, and completed credits.

    Uses the stage thresholds from settings. Falls back to year/semester
    if credit-based detection is ambiguous.
    """
    # Credit-based detection
    stage = ACADEMIC_STAGE_THRESHOLDS[0][1]  # Default to first stage
    for min_credits, stage_name in ACADEMIC_STAGE_THRESHOLDS:
        if completed_credits >= min_credits:
            stage = stage_name

    return stage


def get_stage_numeric(stage: str) -> int:
    """Convert a stage string to a numeric value for comparison."""
    for i, (_, stage_name) in enumerate(ACADEMIC_STAGE_THRESHOLDS):
        if stage_name == stage:
            return i
    return 0


def build_academic_profile(
    student_id: int,
    degree: str,
    year: int,
    semester: int,
    course_records: List[Dict],
) -> AcademicProfile:
    """
    Build a complete academic profile from student data.

    This is the main entry point for profile construction.
    """
    # Build typed course objects
    student_courses = build_student_courses(course_records)

    # Calculate GPA
    gpa, credits_earned, credits_attempted = calculate_gpa(
        course_records
    )

    # Aggregate subject performances
    subject_performances = aggregate_subject_performance(student_courses)

    # Count completed courses
    completed = [
        c for c in student_courses
        if c.status == CourseStatus.COMPLETED.value
    ]

    # Detect academic stage
    academic_stage = detect_academic_stage(year, semester, credits_earned)

    return AcademicProfile(
        student_id=student_id,
        degree=degree,
        year=year,
        semester=semester,
        completed_courses=completed,
        subject_performances=subject_performances,
        gpa=gpa,
        total_credits=credits_earned,
        academic_stage=academic_stage,
        completed_course_count=len(completed),
    )
