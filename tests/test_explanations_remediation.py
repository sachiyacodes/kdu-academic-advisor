"""
Tests for explanation engine remediations.
Verifies the fix for the contribution weight weakness bug and counterfactual generation.
"""
import pytest
from src.ai.explanations import generate_explanation, generate_all_explanations
from src.models.schemas import SpecializationScore


class TestExplanationRemediations:
    def test_high_score_low_weight_never_flagged_as_weakness(self):
        """
        REGRESSION TEST: If a student scores 100% in Mathematics (which has weight 0.05 in Cyber Security),
        contribution is 0.05 * 100 = 5.0 points. This must NEVER be flagged as a weakness!
        """
        score = SpecializationScore(
            specialization_name="Cyber Security",
            academic_fit=88.0,
            interest_alignment=80.0,
            final_score=85.6,
            evidence_level="Moderate Evidence",
            relevant_course_count=6,
            available_subject_areas=["Cyber Security", "Networking", "Mathematics"],
            missing_subject_areas=[],
            subject_contributions={"Cyber Security": 35.0, "Networking": 25.0, "Mathematics": 5.0},
            subject_marks={"Cyber Security": 90.0, "Networking": 85.0, "Mathematics": 100.0},
            rank=1,
        )

        exp = generate_explanation(score, [score])
        weakness_text = " ".join(exp.weaknesses).lower()

        # Mathematics had a 100% score; it should NOT be in weaknesses
        assert "mathematics" not in weakness_text, "A 100% mark in Mathematics was falsely flagged as a weakness!"

    def test_actual_low_mark_is_flagged_as_weakness(self):
        """If a student actually scored poorly (<60) in an area, it should be noted as a weakness."""
        score = SpecializationScore(
            specialization_name="Software Engineering",
            academic_fit=65.0,
            interest_alignment=70.0,
            final_score=66.5,
            evidence_level="Moderate Evidence",
            relevant_course_count=5,
            available_subject_areas=["Programming", "Database"],
            missing_subject_areas=[],
            subject_contributions={"Programming": 25.0, "Database": 4.5},
            subject_marks={"Programming": 85.0, "Database": 45.0},
            rank=1,
        )

        exp = generate_explanation(score, [score])
        weakness_text = " ".join(exp.weaknesses).lower()

        assert "database" in weakness_text
        assert "below" in weakness_text or "low" in weakness_text

    def test_counterfactual_generation_for_runner_up(self):
        """Specializations ranked #2 should have actionable counterfactual advice to bridge the gap."""
        top_score = SpecializationScore(
            specialization_name="Data Science",
            academic_fit=85.0,
            interest_alignment=80.0,
            final_score=83.5,
            rank=1,
        )
        runner_up = SpecializationScore(
            specialization_name="AI / ML",
            academic_fit=80.0,
            interest_alignment=80.0,
            final_score=80.0,
            evidence_level="Moderate Evidence",
            relevant_course_count=5,
            available_subject_areas=["Mathematics", "Programming"],
            subject_contributions={"Mathematics": 22.0, "Programming": 20.0},
            subject_marks={"Mathematics": 78.0, "Programming": 80.0},
            rank=2,
        )

        exp = generate_explanation(runner_up, [top_score, runner_up])
        assert len(exp.counterfactuals) > 0
        assert "Actionable Pathway" in exp.counterfactuals[0]
