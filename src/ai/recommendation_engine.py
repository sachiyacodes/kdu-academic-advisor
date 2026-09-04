"""
Hybrid Recommendation Engine — combines Academic Fit and Interest Alignment.

Formula (section 7, FIX-2):
    Final Compatibility Score = Academic Fit * ACADEMIC_WEIGHT + Interest Alignment * INTEREST_WEIGHT

DISCLOSED ENHANCEMENT (section 4a, row 5):
    The 70/30 Academic Fit / Interest Alignment split is NOT sourced from the proposal.
    The proposal defines both scores but does not specify a numeric combination ratio.
    This is the simplest defensible default for a hybrid recommender and is fully
    configurable in src/config/settings.py.

This module orchestrates the full recommendation pipeline (section 22).
"""

from typing import Any, Dict, List, Optional, Tuple

from src.ai.interest_matching import score_interests_all_specializations
from src.ai.weighted_scoring import score_all_specializations
from src.config.settings import (
    ACADEMIC_WEIGHT,
    INTEREST_WEIGHT,
    SPECIALIZATION_INTEREST_VECTORS,
    SPECIALIZATION_WEIGHTS,
)
from src.models.schemas import AcademicProfile, SpecializationScore


def combine_scores(
    academic_fit: float,
    interest_alignment: float,
    academic_weight: float = ACADEMIC_WEIGHT,
    interest_weight: float = INTEREST_WEIGHT,
) -> float:
    """
    Combine academic fit and interest alignment into a final compatibility score.

    Args:
        academic_fit: Academic Fit score (0-100).
        interest_alignment: Interest Alignment score (0-100).
        academic_weight: Weight for academic fit (default 0.70, configurable).
        interest_weight: Weight for interest alignment (default 0.30, configurable).

    Returns:
        Final Compatibility Score (0-100).
    """
    return round(
        academic_fit * academic_weight + interest_alignment * interest_weight,
        2,
    )


def generate_recommendations(
    profile: AcademicProfile,
    selected_interests: List[str],
    specialization_weights: Optional[Dict[str, Dict[str, float]]] = None,
    specialization_interests: Optional[Dict[str, Dict[str, float]]] = None,
    academic_weight: float = ACADEMIC_WEIGHT,
    interest_weight: float = INTEREST_WEIGHT,
) -> List[SpecializationScore]:
    """
    Run the full recommendation pipeline for a student.

    Pipeline (section 22):
        1. Weighted Academic Scoring (AI Concept 2)
        2. Content-Based Interest Matching (AI Concept 3)
        3. Hybrid Compatibility Calculation (70/30 configurable)
        4. Ranking

    Args:
        profile: Student's academic profile.
        selected_interests: List of selected interest subject area names.
        specialization_weights: Override weights (default: from settings).
        specialization_interests: Override interest vectors (default: from settings).
        academic_weight: Override academic weight (default: 0.70).
        interest_weight: Override interest weight (default: 0.30).

    Returns:
        List of SpecializationScore objects, sorted by final_score descending.
    """
    # Use defaults from settings if not overridden
    spec_weights = specialization_weights or SPECIALIZATION_WEIGHTS
    spec_interests = specialization_interests or SPECIALIZATION_INTEREST_VECTORS

    # Step 1: Weighted Academic Scoring
    academic_scores = score_all_specializations(profile, spec_weights)

    # Step 2: Content-Based Interest Matching
    interest_results = score_interests_all_specializations(
        selected_interests, spec_interests
    )

    # Step 3: Combine scores using configurable weights
    for score in academic_scores:
        spec_name = score.specialization_name
        interest_score, interest_contribs = interest_results.get(
            spec_name, (0.0, {})
        )

        score.interest_alignment = interest_score
        score.interest_contributions = interest_contribs
        score.final_score = combine_scores(
            score.academic_fit,
            score.interest_alignment,
            academic_weight,
            interest_weight,
        )

    # Step 4: Rank by final score (descending)
    academic_scores.sort(key=lambda s: s.final_score, reverse=True)
    for i, score in enumerate(academic_scores):
        score.rank = i + 1

    return academic_scores


def calculate_sensitivity_analysis(
    profile: AcademicProfile,
    selected_interests: Any,
) -> Dict[str, Any]:
    """
    Evaluate stability of recommendations as Academic Weight varies from 0.0 to 1.0 (steps of 0.1).
    Returns weight points, per-specialization trajectories, and stability score.
    """
    weight_points = [round(w * 0.1, 1) for w in range(11)]  # 0.0 to 1.0
    trajectories: Dict[str, List[float]] = {s: [] for s in SPECIALIZATION_WEIGHTS.keys()}
    top_picks: List[str] = []

    for w_acad in weight_points:
        w_int = round(1.0 - w_acad, 2)
        recs = generate_recommendations(
            profile, selected_interests,
            academic_weight=w_acad, interest_weight=w_int
        )
        for r in recs:
            trajectories[r.specialization_name].append(r.final_score)
        if recs:
            top_picks.append(recs[0].specialization_name)

    # Baseline top pick at standard 0.70 weight (index 7 in [0.0..1.0])
    baseline_top = top_picks[7] if len(top_picks) > 7 else (top_picks[0] if top_picks else "")
    stability_pct = round((top_picks.count(baseline_top) / len(top_picks)) * 100, 1) if top_picks else 100.0

    return {
        "academic_weights": weight_points,
        "trajectories": trajectories,
        "top_picks": top_picks,
        "baseline_top": baseline_top,
        "stability_percentage": stability_pct,
    }
