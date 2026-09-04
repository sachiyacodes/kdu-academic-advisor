"""
Data models for the AI-Based IT Specialization & Course Recommendation System.

Uses dataclasses for lightweight, clear data structures.
Pydantic is used only where genuine validation adds value (student input).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# =============================================================================
# Core Data Models (dataclasses — lightweight, no validation overhead)
# =============================================================================

@dataclass
class Course:
    """Represents a course in the curriculum."""
    course_id: int
    course_code: str
    course_name: str
    degree: str
    year: int
    semester: int
    credits: int
    subject_area: str
    course_type: str = "Core"


@dataclass
class StudentCourse:
    """Represents a student's record for a completed/attempted course."""
    student_id: int
    course_id: int
    course_code: str
    course_name: str
    credits: int
    subject_area: str
    mark: float
    grade: str
    grade_point: float
    status: str
    course_type: str = "Core"


@dataclass
class SpecializationWeight:
    """A single weight entry for a specialization's academic scoring."""
    specialization_id: int
    specialization_name: str
    subject_area: str
    weight: float


@dataclass
class SpecializationInterest:
    """A single interest weight entry for a specialization's interest profile."""
    specialization_id: int
    specialization_name: str
    subject_area: str
    weight: float


@dataclass
class Prerequisite:
    """A prerequisite relationship between two courses."""
    course_id: int
    prerequisite_course_id: int


@dataclass
class SpecializationInfo:
    """Specialization metadata."""
    specialization_id: int
    name: str
    description: str


# =============================================================================
# Academic Profile (built from student data)
# =============================================================================

@dataclass
class SubjectPerformance:
    """Aggregated performance in a single subject area."""
    subject_area: str
    average_mark: float
    course_count: int
    total_credits: int
    courses: List[StudentCourse] = field(default_factory=list)


@dataclass
class AcademicProfile:
    """Complete academic profile for a student."""
    student_id: int
    degree: str
    year: int
    semester: int
    completed_courses: List[StudentCourse] = field(default_factory=list)
    subject_performances: Dict[str, SubjectPerformance] = field(default_factory=dict)
    gpa: float = 0.0
    total_credits: int = 0
    academic_stage: str = ""
    completed_course_count: int = 0


# =============================================================================
# Recommendation Results
# =============================================================================

@dataclass
class SpecializationScore:
    """Score breakdown for a single specialization."""
    specialization_name: str
    academic_fit: float = 0.0
    interest_alignment: float = 0.0
    final_score: float = 0.0
    evidence_level: str = "Limited Evidence"
    relevant_course_count: int = 0
    available_subject_areas: List[str] = field(default_factory=list)
    missing_subject_areas: List[str] = field(default_factory=list)
    subject_contributions: Dict[str, float] = field(default_factory=dict)
    subject_marks: Dict[str, float] = field(default_factory=dict)
    interest_contributions: Dict[str, float] = field(default_factory=dict)
    rank: int = 0
    calibrated_fit: float = 0.0
    confidence_score: float = 1.0
    confidence_level: str = "High Evidence"


@dataclass
class CourseRecommendation:
    """A single course recommendation with its status and reasoning."""
    course: Course
    category: str  # "Recommended Now", "Recommended Later", "Low Priority"
    reason: str
    missing_prerequisites: List[str] = field(default_factory=list)
    prerequisite_status: str = "satisfied"
    chain_impact_count: int = 0
    synergy_score: float = 0.0
    target_specialization: str = ""


@dataclass
class Explanation:
    """Explainable recommendation for a specialization."""
    specialization_name: str
    summary: str
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    interest_matches: List[str] = field(default_factory=list)
    evidence_note: str = ""
    missing_areas_note: str = ""
    comparison_notes: List[str] = field(default_factory=list)
    counterfactuals: List[str] = field(default_factory=list)


# =============================================================================
# Validated Input Models (Pydantic — genuine validation value)
# =============================================================================

class FeedbackInput(BaseModel):
    """Validated recommendation feedback input from the UI."""
    student_id: Optional[int] = None
    specialization_name: str
    rating: int = Field(ge=-1, le=1)  # 1 for helpful, -1 for not helpful
    comment: str = ""

class StudentInput(BaseModel):
    """Validated student profile input from the UI."""
    degree: str
    year: int = Field(ge=1, le=4)
    semester: int = Field(ge=1, le=2)

    @field_validator("degree")
    @classmethod
    def validate_degree(cls, v: str) -> str:
        from src.config.settings import DEGREE_PROGRAMS
        if v not in DEGREE_PROGRAMS:
            raise ValueError(f"Degree must be one of: {DEGREE_PROGRAMS}")
        return v


class CourseInput(BaseModel):
    """Validated course mark input from the UI."""
    course_id: int
    mark: float = Field(ge=0, le=100)

    @field_validator("mark")
    @classmethod
    def validate_mark(cls, v: float) -> float:
        if v < 0 or v > 100:
            raise ValueError("Mark must be between 0 and 100")
        return round(v, 1)
