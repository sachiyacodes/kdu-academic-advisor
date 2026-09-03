"""
Weighted Knowledge-Based Scoring Engine — AI Concept 2.

Evaluates how well a student's academic profile matches each specialization
based on subject-area performance and specialization-specific weights.

Formula (matches proposal section 7 exactly):
    Score(s) = Sum(weight_i * normalized_mark_i) / Sum(weight_i)
    where the sum is taken ONLY over subject areas where the student
    has completed courses.

Critical rule (section 16): A missing subject area NEVER receives a score of zero.
Instead, it is excluded from both numerator and denominator, and the remaining
weights are renormalized.

Output is a Specialization Compatibility Score (0-100), NOT a probability.
"""

from typing import Dict, List, Optional, Set, Tuple

from src.config.settings import (
    LIMITED_EVIDENCE_MAX,
    MODERATE_EVIDENCE_MAX,
    STRONG_EVIDENCE_MIN,
    SubjectArea,
)
from src.models.schemas import AcademicProfile, SpecializationScore, SubjectPerformance


def calculate_academic_fit(
    subject_performances: Dict[str, SubjectPerformance],
    specialization_weights: Dict[str, float],
) -> Tuple[float, Dict[str, float], List[str], List[str]]:
    """
    Calculate the Academic Fit score for one specialization.

    Args:
        subject_performances: Student's performance by subject area.
        specialization_weights: Weight dict for this specialization {area: weight}.

    Returns:
        Tuple of:
            - academic_fit_score (0-100)
            - subject_contributions: {area: contribution_value}
            - available_areas: subject areas with student data
            - missing_areas: subject areas without student data

    Missing subject handling (section 16):
        1. Exclude missing areas from numerator AND denominator
        2. Renormalize remaining weights to sum to 1.0
        3. Record which areas were unavailable
    """
    available_areas = []
    missing_areas = []
    subject_contributions = {}

    # Separate available vs missing subject areas
    active_weights = {}
    for area, weight in specialization_weights.items():
        if area in subject_performances:
            available_areas.append(area)
            active_weights[area] = weight
        else:
            missing_areas.append(area)

    # If no data at all, return zero with full missing list
    if not active_weights:
        return 0.0, {}, [], list(specialization_weights.keys())

    # Renormalize weights (section 16, step 3)
    total_active_weight = sum(active_weights.values())
    if total_active_weight == 0:
        return 0.0, {}, available_areas, missing_areas

    normalized_weights = {
        area: w / total_active_weight for area, w in active_weights.items()
    }

    # Calculate weighted score
    # Score(s) = Sum(normalized_weight_i * average_mark_i)
    weighted_sum = 0.0
    for area, norm_weight in normalized_weights.items():
        avg_mark = subject_performances[area].average_mark
        contribution = norm_weight * avg_mark
        weighted_sum += contribution
        subject_contributions[area] = round(contribution, 2)

    academic_fit = round(weighted_sum, 2)

    return academic_fit, subject_contributions, available_areas, missing_areas


def determine_evidence_level(relevant_course_count: int) -> str:
    """
    Determine evidence level based on number of relevant completed courses.

    Section 18:
        Limited Evidence: 0-4 relevant courses
        Moderate Evidence: 5-9 relevant courses
        Strong Evidence: 10+ relevant courses
    """
    if relevant_course_count >= STRONG_EVIDENCE_MIN:
        return "Strong Evidence"
    elif relevant_course_count > LIMITED_EVIDENCE_MAX:
        return "Moderate Evidence"
    else:
        return "Limited Evidence"


def count_relevant_courses(
    profile: AcademicProfile,
    specialization_weights: Dict[str, float],
) -> int:
    """Count completed courses in subject areas relevant to a specialization."""
    relevant_areas = set(specialization_weights.keys())
    count = 0
    for course in profile.completed_courses:
        if course.subject_area in relevant_areas:
            count += 1
    return count


def score_all_specializations(
    profile: AcademicProfile,
    all_specialization_weights: Dict[str, Dict[str, float]],
) -> List[SpecializationScore]:
    """
    Score all specializations for a student's academic profile.

    Returns a list of SpecializationScore objects with academic_fit scores,
    evidence levels, contributions, and available/missing area tracking.
    """
    scores = []

    for spec_name, weights in all_specialization_weights.items():
        # Calculate academic fit
        academic_fit, contributions, available, missing = calculate_academic_fit(
            profile.subject_performances, weights
        )

        # Count relevant courses and determine evidence
        relevant_count = count_relevant_courses(profile, weights)
        evidence = determine_evidence_level(relevant_count)

        score = SpecializationScore(
            specialization_name=spec_name,
            academic_fit=academic_fit,
            evidence_level=evidence,
            relevant_course_count=relevant_count,
            available_subject_areas=available,
            missing_subject_areas=missing,
            subject_contributions=contributions,
        )
        scores.append(score)

    return scores
