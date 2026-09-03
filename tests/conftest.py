"""
Shared test fixtures for the test suite.

Includes deterministic fixtures for manual test scenarios A-E (section 38).
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import SubjectArea, CourseStatus
from src.models.schemas import AcademicProfile, StudentCourse, SubjectPerformance


def make_course(
    student_id: int,
    course_id: int,
    code: str,
    name: str,
    credits: int,
    subject_area: str,
    mark: float,
    grade: str,
    grade_point: float,
    status: str = "completed",
) -> StudentCourse:
    """Helper to create a StudentCourse object."""
    return StudentCourse(
        student_id=student_id,
        course_id=course_id,
        course_code=code,
        course_name=name,
        credits=credits,
        subject_area=subject_area,
        mark=mark,
        grade=grade,
        grade_point=grade_point,
        status=status,
    )


# ========================================================================
# Student A — Data Science profile (section 38)
# Statistics 88, Programming 84, Database 80, Mathematics 76
# Interests: Data Analysis, Statistics
# Expected: Data Science ranks strongly.
# ========================================================================

@pytest.fixture
def student_a_courses():
    """Student A course records — strong Data Science profile."""
    return [
        make_course(1, 1, "IT2102", "Probability and Statistics", 3,
                    SubjectArea.STATISTICS.value, 88, "A", 4.0),
        make_course(1, 2, "IT1101", "Introduction to Programming", 4,
                    SubjectArea.PROGRAMMING.value, 84, "A-", 3.7),
        make_course(1, 3, "IT1203", "Database Fundamentals", 4,
                    SubjectArea.DATABASE.value, 80, "A-", 3.7),
        make_course(1, 4, "IT1102", "Mathematics for Computing I", 3,
                    SubjectArea.MATHEMATICS.value, 76, "B+", 3.3),
    ]


@pytest.fixture
def student_a_interests():
    """Student A interests."""
    return [SubjectArea.DATA_ANALYSIS.value, SubjectArea.STATISTICS.value]


# ========================================================================
# Student B — Cyber Security profile (section 38)
# Cyber Security 91, Networking 86, Programming 78, Systems 84
# Interests: Cyber Security, Networking
# Expected: Cyber Security ranks strongly.
# ========================================================================

@pytest.fixture
def student_b_courses():
    """Student B course records — strong Cyber Security profile."""
    return [
        make_course(2, 1, "IT3102", "Information Security", 3,
                    SubjectArea.CYBER_SECURITY.value, 91, "A+", 4.0),
        make_course(2, 2, "IT1204", "Introduction to Networking", 3,
                    SubjectArea.NETWORKING.value, 86, "A", 4.0),
        make_course(2, 3, "IT1101", "Introduction to Programming", 4,
                    SubjectArea.PROGRAMMING.value, 78, "B+", 3.3),
        make_course(2, 4, "IT2103", "Operating Systems", 3,
                    SubjectArea.SYSTEMS_OS.value, 84, "A-", 3.7),
    ]


@pytest.fixture
def student_b_interests():
    """Student B interests."""
    return [SubjectArea.CYBER_SECURITY.value, SubjectArea.NETWORKING.value]


# ========================================================================
# Student C — Software Engineering profile (section 38)
# Programming 92, Software Engineering 88, Algorithms 84, Database 75
# Interest: Programming (mapped to Software Development concept)
# Expected: Software Engineering ranks strongly.
# ========================================================================

@pytest.fixture
def student_c_courses():
    """Student C course records — strong Software Engineering profile."""
    return [
        make_course(3, 1, "IT1101", "Introduction to Programming", 4,
                    SubjectArea.PROGRAMMING.value, 92, "A+", 4.0),
        make_course(3, 2, "IT2104", "Software Engineering Principles", 3,
                    SubjectArea.SOFTWARE_ENGINEERING.value, 88, "A", 4.0),
        make_course(3, 3, "IT2101", "Data Structures and Algorithms", 4,
                    SubjectArea.ALGORITHMS_DS.value, 84, "A-", 3.7),
        make_course(3, 4, "IT1203", "Database Fundamentals", 4,
                    SubjectArea.DATABASE.value, 75, "B+", 3.3),
    ]


@pytest.fixture
def student_c_interests():
    """Student C interests."""
    return [SubjectArea.PROGRAMMING.value]


# ========================================================================
# Student D — Conflicting profile (section 38)
# Strong Programming 90, strong Statistics 85, moderate Security 70
# Interests: AI, Data Analysis, Cyber Security
# Expected: meaningful ranked result, not arbitrary single answer
# ========================================================================

@pytest.fixture
def student_d_courses():
    """Student D course records — conflicting profile."""
    return [
        make_course(4, 1, "IT1101", "Introduction to Programming", 4,
                    SubjectArea.PROGRAMMING.value, 90, "A+", 4.0),
        make_course(4, 2, "IT2102", "Probability and Statistics", 3,
                    SubjectArea.STATISTICS.value, 85, "A", 4.0),
        make_course(4, 3, "IT3102", "Information Security", 3,
                    SubjectArea.CYBER_SECURITY.value, 70, "B", 3.0),
    ]


@pytest.fixture
def student_d_interests():
    """Student D interests — spread across multiple areas."""
    return [
        SubjectArea.ARTIFICIAL_INTELLIGENCE.value,
        SubjectArea.DATA_ANALYSIS.value,
        SubjectArea.CYBER_SECURITY.value,
    ]


# ========================================================================
# Student E — Early academic stage (section 38)
# Very few completed courses, limited evidence
# Expected: Limited Evidence, avoids overconfident recommendations
# ========================================================================

@pytest.fixture
def student_e_courses():
    """Student E course records — early stage, limited evidence."""
    return [
        make_course(5, 1, "IT1101", "Introduction to Programming", 4,
                    SubjectArea.PROGRAMMING.value, 72, "B", 3.0),
    ]


@pytest.fixture
def student_e_interests():
    """Student E interests."""
    return []


# ========================================================================
# Helper to build profile from fixtures
# ========================================================================

@pytest.fixture
def build_profile():
    """Factory fixture to build an AcademicProfile from StudentCourse lists."""
    from src.academic.profile import aggregate_subject_performance, detect_academic_stage

    def _build(student_id, courses, degree="Information Technology", year=2, semester=1):
        subject_perfs = aggregate_subject_performance(courses)
        completed = [c for c in courses if c.status == CourseStatus.COMPLETED.value]
        total_credits = sum(c.credits for c in completed)
        stage = detect_academic_stage(year, semester, total_credits)

        return AcademicProfile(
            student_id=student_id,
            degree=degree,
            year=year,
            semester=semester,
            completed_courses=completed,
            subject_performances=subject_perfs,
            gpa=0.0,
            total_credits=total_credits,
            academic_stage=stage,
            completed_course_count=len(completed),
        )

    return _build
