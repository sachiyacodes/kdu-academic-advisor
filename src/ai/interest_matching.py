"""
Content-Based Interest Matching Engine — AI Concept 3 (FIX-3).

Implements interest matching EXACTLY as the proposal defines it in section 7:
- The canonical subject-area taxonomy (section 9) is the shared vector space
  for both scoring and interest matching.
- Each specialization has a fixed interest-to-subject weight vector over that
  same taxonomy (stored in specialization_interests.csv).
- The student's selected interests are converted into a student interest vector
  over the same taxonomy.
- InterestScore(s) = cosine_similarity(student_interest_vector, specialization_interest_vector)
  computed over the shared subject-area space.

The formula uses cosine similarity, normalized to 0-100 for display consistency
with the academic fit score. This is documented in docs/ai_methodology.md.
"""

import math
from typing import Dict, List, Set, Tuple

from src.config.settings import SUBJECT_AREA_ORDER, SubjectArea


def build_student_interest_vector(
    selected_interests: List[str],
) -> List[float]:
    """
    Build a student interest vector over the canonical subject-area taxonomy.

    Each dimension corresponds to a subject area (in SUBJECT_AREA_ORDER).
    Selected interests activate their corresponding dimension with 1.0,
    unselected dimensions are 0.0.

    Args:
        selected_interests: List of subject area names the student selected.

    Returns:
        List of floats (length 13), one per subject area in canonical order.
    """
    vector = []
    for area in SUBJECT_AREA_ORDER:
        if area in selected_interests:
            vector.append(1.0)
        else:
            vector.append(0.0)
    return vector


def build_specialization_interest_vector(
    specialization_interest_weights: Dict[str, float],
) -> List[float]:
    """
    Build a specialization interest vector over the canonical taxonomy.

    Each dimension corresponds to a subject area (in SUBJECT_AREA_ORDER).
    The weight from the specialization's interest profile fills the dimension;
    missing dimensions are 0.0.

    Args:
        specialization_interest_weights: {subject_area: weight} for this specialization.

    Returns:
        List of floats (length 13), one per subject area in canonical order.
    """
    vector = []
    for area in SUBJECT_AREA_ORDER:
        vector.append(specialization_interest_weights.get(area, 0.0))
    return vector


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Returns a value in [0, 1] (both vectors are non-negative).
    Returns 0.0 if either vector has zero magnitude.

    Formula: cos(a, b) = (a . b) / (|a| * |b|)
    """
    if len(vec_a) != len(vec_b):
        raise ValueError(
            f"Vectors must have same length: {len(vec_a)} vs {len(vec_b)}"
        )

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def calculate_interest_score(
    selected_interests: List[str],
    specialization_interest_weights: Dict[str, float],
) -> Tuple[float, Dict[str, float]]:
    """
    Calculate the interest alignment score for one specialization.

    Args:
        selected_interests: List of subject area names the student selected.
        specialization_interest_weights: {subject_area: weight} for this spec.

    Returns:
        Tuple of:
            - interest_score (0-100, cosine similarity * 100)
            - interest_contributions: {area: contribution} for areas that matched

    FIX-3 formula:
        student_vector = [1 if interest in selected else 0, for each area]
        spec_vector = [interest_weight for each area]
        InterestScore = cosine_similarity(student_vector, spec_vector) * 100
    """
    if not selected_interests:
        return 0.0, {}

    student_vec = build_student_interest_vector(selected_interests)
    spec_vec = build_specialization_interest_vector(specialization_interest_weights)

    similarity = cosine_similarity(student_vec, spec_vec)
    score = round(similarity * 100, 2)

    # Identify which interests contributed to the match
    contributions = {}
    for i, area in enumerate(SUBJECT_AREA_ORDER):
        if student_vec[i] > 0 and spec_vec[i] > 0:
            contributions[area] = round(spec_vec[i] * 100, 2)

    return score, contributions


def score_interests_all_specializations(
    selected_interests: List[str],
    all_specialization_interests: Dict[str, Dict[str, float]],
) -> Dict[str, Tuple[float, Dict[str, float]]]:
    """
    Calculate interest scores for all specializations.

    Args:
        selected_interests: List of subject area names the student selected.
        all_specialization_interests: {spec_name: {area: weight}} for all specs.

    Returns:
        Dict of {spec_name: (interest_score, contributions)}.
    """
    results = {}
    for spec_name, interest_weights in all_specialization_interests.items():
        score, contributions = calculate_interest_score(
            selected_interests, interest_weights
        )
        results[spec_name] = (score, contributions)
    return results
