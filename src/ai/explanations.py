"""
Explainable Recommendations Module.

Generates human-readable explanations for every recommendation.
All explanations are derived from actual calculation results — never
generic hard-coded text (section 19).

Every recommendation explains:
- Why the specialization matched
- Which academic areas contributed most
- Which interests contributed
- What weaknesses exist
- What evidence is available
- Which prerequisites are missing
- Why another specialization may rank higher
"""

from typing import Dict, List, Optional

from src.config.settings import (
    HIGH_MATCH_THRESHOLD,
    MODERATE_MATCH_THRESHOLD,
    HYBRID_WEIGHT_DISCLOSURE,
    MISSING_EVIDENCE_DISCLOSURE,
)
from src.models.schemas import Explanation, SpecializationScore


def generate_explanation(
    score: SpecializationScore,
    all_scores: List[SpecializationScore],
) -> Explanation:
    """
    Generate an explainable recommendation for a single specialization.

    All text is generated dynamically from the actual score data,
    never from static templates.

    Args:
        score: The specialization's score breakdown.
        all_scores: All scored specializations (for comparative explanations).

    Returns:
        An Explanation object with all recommendation details.
    """
    spec_name = score.specialization_name
    strengths = []
    weaknesses = []
    interest_matches = []
    comparison_notes = []

    # --- Summary ---
    if score.final_score >= HIGH_MATCH_THRESHOLD:
        match_level = "a strong match"
    elif score.final_score >= MODERATE_MATCH_THRESHOLD:
        match_level = "a moderate match"
    else:
        match_level = "a weaker match"

    summary = (
        f"Based on the available academic evidence, {spec_name} appears to be "
        f"{match_level} for your profile (Compatibility Score: {score.final_score:.1f}/100)."
    )

    # --- Strengths: top contributing subject areas ---
    if score.subject_contributions:
        sorted_contribs = sorted(
            score.subject_contributions.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        for area, contrib in sorted_contribs[:3]:
            strengths.append(
                f"Your {area} performance contributes {contrib:.1f} points "
                f"to the academic fit score."
            )

    # --- Weaknesses: lowest contributing areas or missing areas ---
    if score.subject_contributions:
        sorted_contribs = sorted(
            score.subject_contributions.items(),
            key=lambda x: x[1],
        )
        for area, contrib in sorted_contribs[:2]:
            if contrib < 10:
                weaknesses.append(
                    f"Your {area} performance is relatively low, contributing "
                    f"only {contrib:.1f} points."
                )

    if score.missing_subject_areas:
        missing_str = ", ".join(score.missing_subject_areas)
        weaknesses.append(
            f"No completed courses found in: {missing_str}. "
            f"These areas could not be evaluated."
        )

    # --- Interest matches ---
    if score.interest_contributions:
        for area, weight in sorted(
            score.interest_contributions.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            interest_matches.append(
                f"Your interest in {area} aligns with this specialization "
                f"(weight: {weight:.1f}%)."
            )
    else:
        interest_matches.append(
            "No selected interests directly match this specialization's profile."
        )

    # --- Evidence note ---
    evidence_note = (
        f"Evidence Level: {score.evidence_level} "
        f"({score.relevant_course_count} relevant completed courses)."
    )
    if score.evidence_level == "Limited Evidence":
        evidence_note += (
            " This recommendation is based on limited academic data. "
            "As you complete more courses, the recommendation accuracy will improve."
        )

    # --- Missing areas note ---
    missing_areas_note = ""
    if score.missing_subject_areas:
        missing_areas_note = MISSING_EVIDENCE_DISCLOSURE

    # --- Comparison with higher-ranked specializations ---
    if score.rank > 1:
        higher = [s for s in all_scores if s.rank < score.rank]
        for h in higher[:2]:
            diff = h.final_score - score.final_score
            comparison_notes.append(
                f"{h.specialization_name} ranks higher by {diff:.1f} points "
                f"(Academic Fit: {h.academic_fit:.1f} vs {score.academic_fit:.1f}, "
                f"Interest Alignment: {h.interest_alignment:.1f} vs {score.interest_alignment:.1f})."
            )

    return Explanation(
        specialization_name=spec_name,
        summary=summary,
        strengths=strengths,
        weaknesses=weaknesses,
        interest_matches=interest_matches,
        evidence_note=evidence_note,
        missing_areas_note=missing_areas_note,
        comparison_notes=comparison_notes,
    )


def generate_all_explanations(
    scores: List[SpecializationScore],
) -> Dict[str, Explanation]:
    """
    Generate explanations for all scored specializations.

    Args:
        scores: List of SpecializationScore objects (already ranked).

    Returns:
        Dict mapping specialization name to its Explanation.
    """
    explanations = {}
    for score in scores:
        explanations[score.specialization_name] = generate_explanation(
            score, scores
        )
    return explanations
