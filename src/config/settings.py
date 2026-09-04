"""
Centralized configuration for the AI-Based IT Specialization & Course Recommendation System.

This module is the SINGLE source of truth for all constants, enums, weights,
thresholds, and configuration values. No magic numbers elsewhere in the codebase.

Enhancement Disclosure (§4a):
- The 70/30 Academic Fit / Interest Alignment split is a disclosed enhancement,
  not sourced from the proposal. It is fully configurable here.
"""

from enum import Enum
from typing import Dict, List, Tuple


# =============================================================================
# SUBJECT-AREA TAXONOMY (§9)
# Canonical, single source of truth. These exact names appear in CSV files,
# database records, the scoring engine, the interest-matching engine, the UI,
# charts, documentation, and tests. Never abbreviate or rename.
# =============================================================================

class SubjectArea(str, Enum):
    """Canonical subject-area taxonomy — §9 of the master specification."""
    PROGRAMMING = "Programming"
    MATHEMATICS = "Mathematics"
    STATISTICS = "Statistics"
    DATABASE = "Database"
    NETWORKING = "Networking"
    CYBER_SECURITY = "Cyber Security"
    ALGORITHMS_DS = "Algorithms & Data Structures"
    SOFTWARE_ENGINEERING = "Software Engineering"
    SYSTEMS_OS = "Systems & Operating Systems"
    DATA_ANALYSIS = "Data Analysis"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    CLOUD_COMPUTING = "Cloud Computing"
    OTHER = "Other"


# Ordered list for consistent iteration / vector construction
SUBJECT_AREA_ORDER: List[str] = [sa.value for sa in SubjectArea]


# =============================================================================
# SPECIALIZATIONS (§10)
# Prototype specialization categories — not necessarily official KDU names
# unless verified against official curriculum documentation.
# =============================================================================

class Specialization(str, Enum):
    """Prototype specialization categories — §10."""
    SOFTWARE_ENGINEERING = "Software Engineering"
    DATA_SCIENCE = "Data Science"
    AI_ML = "Artificial Intelligence / Machine Learning"
    CYBER_SECURITY = "Cyber Security"
    NETWORKING_CLOUD = "Networking & Cloud Computing"
    DATABASE_ENGINEERING = "Database & Data Engineering"


# =============================================================================
# SPECIALIZATION WEIGHTS (§11 — verified identical to proposal)
# Each specialization's weights MUST sum to 1.00.
# Stored here for reference; authoritative source is specialization_weights.csv.
# =============================================================================

SPECIALIZATION_WEIGHTS: Dict[str, Dict[str, float]] = {
    Specialization.DATA_SCIENCE.value: {
        SubjectArea.STATISTICS.value: 0.30,
        SubjectArea.PROGRAMMING.value: 0.25,
        SubjectArea.DATABASE.value: 0.20,
        SubjectArea.MATHEMATICS.value: 0.15,
        SubjectArea.OTHER.value: 0.10,
    },
    Specialization.AI_ML.value: {
        SubjectArea.MATHEMATICS.value: 0.25,
        SubjectArea.STATISTICS.value: 0.20,
        SubjectArea.PROGRAMMING.value: 0.25,
        SubjectArea.ALGORITHMS_DS.value: 0.15,
        SubjectArea.ARTIFICIAL_INTELLIGENCE.value: 0.15,
    },
    Specialization.CYBER_SECURITY.value: {
        SubjectArea.CYBER_SECURITY.value: 0.35,
        SubjectArea.NETWORKING.value: 0.25,
        SubjectArea.PROGRAMMING.value: 0.20,
        SubjectArea.SYSTEMS_OS.value: 0.15,
        SubjectArea.MATHEMATICS.value: 0.05,
    },
    Specialization.SOFTWARE_ENGINEERING.value: {
        SubjectArea.PROGRAMMING.value: 0.30,
        SubjectArea.SOFTWARE_ENGINEERING.value: 0.25,
        SubjectArea.ALGORITHMS_DS.value: 0.20,
        SubjectArea.DATABASE.value: 0.10,
        SubjectArea.SYSTEMS_OS.value: 0.10,
        SubjectArea.OTHER.value: 0.05,
    },
    Specialization.NETWORKING_CLOUD.value: {
        SubjectArea.NETWORKING.value: 0.40,
        SubjectArea.SYSTEMS_OS.value: 0.20,
        SubjectArea.CYBER_SECURITY.value: 0.15,
        SubjectArea.PROGRAMMING.value: 0.10,
        SubjectArea.CLOUD_COMPUTING.value: 0.15,
    },
    Specialization.DATABASE_ENGINEERING.value: {
        SubjectArea.DATABASE.value: 0.35,
        SubjectArea.PROGRAMMING.value: 0.20,
        SubjectArea.DATA_ANALYSIS.value: 0.15,
        SubjectArea.MATHEMATICS.value: 0.10,
        SubjectArea.STATISTICS.value: 0.10,
        SubjectArea.SYSTEMS_OS.value: 0.10,
    },
}


# =============================================================================
# SPECIALIZATION INTEREST VECTORS (FIX-3)
# Fixed weight vectors over the same 13-item taxonomy for interest matching.
# Used by Content-Based Interest Matching (AI Concept 3).
# =============================================================================

SPECIALIZATION_INTEREST_VECTORS: Dict[str, Dict[str, float]] = {
    Specialization.DATA_SCIENCE.value: {
        SubjectArea.STATISTICS.value: 0.25,
        SubjectArea.PROGRAMMING.value: 0.15,
        SubjectArea.DATABASE.value: 0.15,
        SubjectArea.MATHEMATICS.value: 0.15,
        SubjectArea.DATA_ANALYSIS.value: 0.20,
        SubjectArea.ARTIFICIAL_INTELLIGENCE.value: 0.10,
    },
    Specialization.AI_ML.value: {
        SubjectArea.ARTIFICIAL_INTELLIGENCE.value: 0.25,
        SubjectArea.MATHEMATICS.value: 0.20,
        SubjectArea.PROGRAMMING.value: 0.20,
        SubjectArea.STATISTICS.value: 0.15,
        SubjectArea.ALGORITHMS_DS.value: 0.10,
        SubjectArea.DATA_ANALYSIS.value: 0.10,
    },
    Specialization.CYBER_SECURITY.value: {
        SubjectArea.CYBER_SECURITY.value: 0.30,
        SubjectArea.NETWORKING.value: 0.25,
        SubjectArea.SYSTEMS_OS.value: 0.15,
        SubjectArea.PROGRAMMING.value: 0.15,
        SubjectArea.CLOUD_COMPUTING.value: 0.10,
        SubjectArea.OTHER.value: 0.05,
    },
    Specialization.SOFTWARE_ENGINEERING.value: {
        SubjectArea.PROGRAMMING.value: 0.25,
        SubjectArea.SOFTWARE_ENGINEERING.value: 0.25,
        SubjectArea.ALGORITHMS_DS.value: 0.15,
        SubjectArea.DATABASE.value: 0.10,
        SubjectArea.SYSTEMS_OS.value: 0.10,
        SubjectArea.CLOUD_COMPUTING.value: 0.05,
        SubjectArea.OTHER.value: 0.10,
    },
    Specialization.NETWORKING_CLOUD.value: {
        SubjectArea.NETWORKING.value: 0.30,
        SubjectArea.CLOUD_COMPUTING.value: 0.25,
        SubjectArea.SYSTEMS_OS.value: 0.15,
        SubjectArea.CYBER_SECURITY.value: 0.15,
        SubjectArea.PROGRAMMING.value: 0.10,
        SubjectArea.OTHER.value: 0.05,
    },
    Specialization.DATABASE_ENGINEERING.value: {
        SubjectArea.DATABASE.value: 0.30,
        SubjectArea.PROGRAMMING.value: 0.15,
        SubjectArea.DATA_ANALYSIS.value: 0.20,
        SubjectArea.MATHEMATICS.value: 0.10,
        SubjectArea.STATISTICS.value: 0.10,
        SubjectArea.SYSTEMS_OS.value: 0.10,
        SubjectArea.OTHER.value: 0.05,
    },
}


# =============================================================================
# HYBRID RECOMMENDATION WEIGHTS (§7, FIX-2)
# DISCLOSED ENHANCEMENT: The proposal defines Academic Fit and Interest Alignment
# as two separate scores but does not specify a numeric combination ratio.
# The 70/30 split is the simplest defensible default for a hybrid recommender.
# It is fully configurable here and never hard-coded elsewhere.
# =============================================================================

ACADEMIC_WEIGHT: float = 0.70
INTEREST_WEIGHT: float = 0.30


# =============================================================================
# GRADING SCALE (§13)
# Prototype grading scale — NOT official KDU grading policy unless verified.
# Editable configuration: list of (min_mark, max_mark, grade, grade_point).
# =============================================================================

GRADING_SCALE: List[Tuple[int, int, str, float]] = [
    (90, 100, "A+", 4.0),
    (85, 89,  "A",  4.0),
    (80, 84,  "A-", 3.7),
    (75, 79,  "B+", 3.3),
    (70, 74,  "B",  3.0),
    (65, 69,  "B-", 2.7),
    (60, 64,  "C+", 2.3),
    (55, 59,  "C",  2.0),
    (50, 54,  "C-", 1.7),
    (40, 49,  "D",  1.0),
    (0,  39,  "F",  0.0),
]


# =============================================================================
# EVIDENCE LEVEL THRESHOLDS (§18)
# =============================================================================

LIMITED_EVIDENCE_MAX: int = 4
MODERATE_EVIDENCE_MAX: int = 9
STRONG_EVIDENCE_MIN: int = 10


# =============================================================================
# COURSE STATUSES
# =============================================================================

class CourseStatus(str, Enum):
    """Possible statuses for a student-course record."""
    COMPLETED = "completed"
    FAILED = "failed"
    WITHDRAWN = "withdrawn"
    IN_PROGRESS = "in_progress"


# =============================================================================
# DEGREE PROGRAMS (§8)
# =============================================================================

DEGREE_PROGRAMS: List[str] = [
    "Information Technology",
    "Software Engineering",
    "Computer Science",
    "Data Science & Business Analytics",
    "Information Systems",
    "Computer Engineering",
]


# =============================================================================
# ACADEMIC STAGE THRESHOLDS
# Determines student academic stage based on completed credits.
# Disclosed enhancement: specific credit thresholds are prototype values.
# =============================================================================

ACADEMIC_STAGE_THRESHOLDS: List[Tuple[int, str]] = [
    (0, "Year 1 - Semester 1"),
    (15, "Year 1 - Semester 2"),
    (30, "Year 2 - Semester 1"),
    (45, "Year 2 - Semester 2"),
    (60, "Year 3 - Semester 1"),
    (75, "Year 3 - Semester 2"),
    (90, "Year 4 - Semester 1"),
    (105, "Year 4 - Semester 2"),
]


# =============================================================================
# RECOMMENDATION THRESHOLDS
# =============================================================================

HIGH_MATCH_THRESHOLD: float = 75.0
MODERATE_MATCH_THRESHOLD: float = 50.0
LOW_MATCH_THRESHOLD: float = 25.0


# =============================================================================
# MINIMUM PASS MARK
# =============================================================================

MINIMUM_PASS_MARK: int = 40


# =============================================================================
# DATABASE
# =============================================================================

DATABASE_PATH: str = "database/academic.db"
DATA_DIR: str = "data"


# =============================================================================
# SYNTHETIC DATA
# =============================================================================

SYNTHETIC_SEED: int = 42
SYNTHETIC_STUDENT_COUNT: int = 750


# =============================================================================
# ML ENHANCEMENT & BENCHMARKING
# =============================================================================

ML_TEST_SIZE: float = 0.2
ML_RANDOM_STATE: int = 42
ML_CV_FOLDS: int = 5
MIN_ML_CONFIDENCE_THRESHOLD: float = 0.35
PRIOR_ACADEMIC_MEAN: float = 65.0
INTEREST_DEFAULT_INTENSITY: float = 3.0


# =============================================================================
# APPLICATION METADATA
# =============================================================================

APP_TITLE: str = "AI-Based IT Specialization & Course Recommendation System"
APP_SUBTITLE: str = "KDU — IT3182 Essentials of Artificial Intelligence — Group 22"
APP_VERSION: str = "1.0.0"

DISCLAIMER: str = (
    "This system provides academic decision support based on the information "
    "entered by the student and the prototype's predefined rules and weighting "
    "model. Recommendations are not guaranteed outcomes and should not replace "
    "official academic guidance. The grading scale and curriculum data used in "
    "this prototype are illustrative and may not represent official KDU academic "
    "policies."
)

HYBRID_WEIGHT_DISCLOSURE: str = (
    "Academic Fit / Interest Alignment weighting (70/30) is a configurable "
    "prototype default."
)

SYNTHETIC_DATA_DISCLAIMER: str = (
    "The dataset is synthetic, intended for demonstration and evaluation of "
    "the prototype. Results cannot be assumed to represent real KDU students."
)

MISSING_EVIDENCE_DISCLOSURE: str = (
    "This recommendation is based on available completed-course evidence. "
    "Some subject areas have insufficient academic evidence."
)
