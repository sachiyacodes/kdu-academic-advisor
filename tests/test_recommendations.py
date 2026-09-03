"""
Tests for the hybrid recommendation engine.

Verifies the 70/30 combination (FIX-2), configurability, and ranking.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.recommendation_engine import combine_scores, generate_recommendations
from src.config.settings import ACADEMIC_WEIGHT, INTEREST_WEIGHT, SPECIALIZATION_WEIGHTS


class TestCombineScores:
    def test_default_weights(self):
        """Test 70/30 split with default weights."""
        result = combine_scores(80.0, 90.0)
        expected = 80.0 * 0.70 + 90.0 * 0.30  # 56 + 27 = 83
        assert result == pytest.approx(expected, abs=0.01)

    def test_custom_weights(self):
        """Test with custom weights to verify configurability."""
        result = combine_scores(80.0, 90.0, academic_weight=0.5, interest_weight=0.5)
        expected = 80.0 * 0.5 + 90.0 * 0.5  # 40 + 45 = 85
        assert result == pytest.approx(expected, abs=0.01)

    def test_zero_academic(self):
        """Zero academic fit, full interest."""
        result = combine_scores(0.0, 100.0)
        assert result == pytest.approx(30.0, abs=0.01)

    def test_zero_interest(self):
        """Full academic fit, zero interest."""
        result = combine_scores(100.0, 0.0)
        assert result == pytest.approx(70.0, abs=0.01)

    def test_both_zero(self):
        assert combine_scores(0.0, 0.0) == 0.0

    def test_both_hundred(self):
        assert combine_scores(100.0, 100.0) == pytest.approx(100.0, abs=0.01)


class TestWeightConfiguration:
    """Verify the 70/30 default is as disclosed (FIX-2)."""

    def test_academic_weight_is_070(self):
        assert ACADEMIC_WEIGHT == 0.70

    def test_interest_weight_is_030(self):
        assert INTEREST_WEIGHT == 0.30

    def test_weights_sum_to_one(self):
        assert ACADEMIC_WEIGHT + INTEREST_WEIGHT == pytest.approx(1.0, abs=0.001)


class TestRecommendationRanking:
    """Test that recommendations are correctly ranked."""

    def test_student_a_data_science_top(
        self, student_a_courses, student_a_interests, build_profile
    ):
        """Student A (Data Science profile) should rank Data Science highly."""
        profile = build_profile(1, student_a_courses)
        scores = generate_recommendations(profile, student_a_interests)

        # Data Science should be in top 2 for Student A
        top_names = [s.specialization_name for s in scores[:2]]
        assert "Data Science" in top_names

    def test_student_b_cyber_security_top(
        self, student_b_courses, student_b_interests, build_profile
    ):
        """Student B (Cyber Security profile) should rank Cyber Security top."""
        profile = build_profile(2, student_b_courses)
        scores = generate_recommendations(profile, student_b_interests)

        assert scores[0].specialization_name == "Cyber Security"

    def test_student_c_software_engineering_top(
        self, student_c_courses, student_c_interests, build_profile
    ):
        """Student C (Software Engineering profile) should rank SE highly."""
        profile = build_profile(3, student_c_courses)
        scores = generate_recommendations(profile, student_c_interests)

        top_names = [s.specialization_name for s in scores[:2]]
        assert "Software Engineering" in top_names

    def test_student_d_meaningful_ranking(
        self, student_d_courses, student_d_interests, build_profile
    ):
        """Student D (conflicting profile) should produce meaningful, non-equal rankings."""
        profile = build_profile(4, student_d_courses)
        scores = generate_recommendations(profile, student_d_interests)

        # Should have 6 specializations ranked
        assert len(scores) == 6
        # Ranks should be 1-6
        ranks = [s.rank for s in scores]
        assert sorted(ranks) == [1, 2, 3, 4, 5, 6]
        # All scores should have explanatory data
        for s in scores:
            assert s.final_score >= 0

    def test_student_e_limited_evidence(
        self, student_e_courses, student_e_interests, build_profile
    ):
        """Student E (early stage) should have Limited Evidence for all."""
        profile = build_profile(5, student_e_courses, year=1, semester=1)
        scores = generate_recommendations(profile, student_e_interests)

        for score in scores:
            assert score.evidence_level == "Limited Evidence"

    def test_score_breakdown_displayed(
        self, student_a_courses, student_a_interests, build_profile
    ):
        """Each score should have academic_fit, interest_alignment, and final_score."""
        profile = build_profile(1, student_a_courses)
        scores = generate_recommendations(profile, student_a_interests)

        for score in scores:
            assert hasattr(score, "academic_fit")
            assert hasattr(score, "interest_alignment")
            assert hasattr(score, "final_score")
            assert score.final_score == pytest.approx(
                score.academic_fit * 0.70 + score.interest_alignment * 0.30,
                abs=0.01,
            )
