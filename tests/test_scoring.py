"""
Tests for the weighted scoring engine (AI Concept 2).

Tests weight normalization, missing subject handling (section 16),
and scoring against manual test scenarios.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.weighted_scoring import (
    calculate_academic_fit,
    determine_evidence_level,
    count_relevant_courses,
    score_all_specializations,
)
from src.config.settings import SPECIALIZATION_WEIGHTS, SubjectArea
from src.models.schemas import SubjectPerformance


class TestWeightValidation:
    """Verify all specialization weights sum to 1.0 (section 11)."""

    @pytest.mark.parametrize("spec_name", list(SPECIALIZATION_WEIGHTS.keys()))
    def test_weights_sum_to_one(self, spec_name):
        weights = SPECIALIZATION_WEIGHTS[spec_name]
        total = sum(weights.values())
        assert abs(total - 1.0) < 0.001, \
            f"{spec_name} weights sum to {total}, expected 1.0"


class TestAcademicFit:
    def test_perfect_scores_all_areas(self):
        """Student with 100 in all areas should get 100."""
        weights = {"Programming": 0.5, "Mathematics": 0.5}
        perfs = {
            "Programming": SubjectPerformance("Programming", 100.0, 3, 12),
            "Mathematics": SubjectPerformance("Mathematics", 100.0, 2, 6),
        }
        score, contribs, available, missing = calculate_academic_fit(perfs, weights)
        assert score == pytest.approx(100.0, abs=0.1)
        assert len(missing) == 0

    def test_zero_scores(self):
        """Student with 0 in all areas should get 0."""
        weights = {"Programming": 0.5, "Mathematics": 0.5}
        perfs = {
            "Programming": SubjectPerformance("Programming", 0.0, 1, 3),
            "Mathematics": SubjectPerformance("Mathematics", 0.0, 1, 3),
        }
        score, _, _, _ = calculate_academic_fit(perfs, weights)
        assert score == 0.0

    def test_missing_subject_excluded(self):
        """
        Missing subject area must NOT receive zero (section 16).
        Weights must be renormalized.
        """
        weights = {"Programming": 0.5, "Mathematics": 0.3, "Statistics": 0.2}
        perfs = {
            "Programming": SubjectPerformance("Programming", 80.0, 2, 6),
            # Mathematics and Statistics are missing
        }
        score, contribs, available, missing = calculate_academic_fit(perfs, weights)

        # Only Programming is available, so its weight is renormalized to 1.0
        # Score should be 80.0, NOT 0.5 * 80 = 40 (which would be wrong)
        assert score == pytest.approx(80.0, abs=0.1)
        assert "Mathematics" in missing
        assert "Statistics" in missing
        assert "Programming" in available

    def test_partial_data(self):
        """With 2 of 3 areas, weights should renormalize."""
        weights = {"Programming": 0.5, "Mathematics": 0.3, "Statistics": 0.2}
        perfs = {
            "Programming": SubjectPerformance("Programming", 80.0, 2, 6),
            "Mathematics": SubjectPerformance("Mathematics", 60.0, 1, 3),
        }
        score, contribs, available, missing = calculate_academic_fit(perfs, weights)

        # Renormalized weights: Prog=0.5/0.8=0.625, Math=0.3/0.8=0.375
        expected = 0.625 * 80.0 + 0.375 * 60.0
        assert score == pytest.approx(expected, abs=0.1)
        assert "Statistics" in missing

    def test_no_data(self):
        """No student data should return 0 with everything missing."""
        weights = {"Programming": 0.5, "Mathematics": 0.5}
        perfs = {}
        score, contribs, available, missing = calculate_academic_fit(perfs, weights)
        assert score == 0.0
        assert len(missing) == 2


class TestEvidenceLevel:
    def test_limited(self):
        assert determine_evidence_level(0) == "Limited Evidence"
        assert determine_evidence_level(4) == "Limited Evidence"

    def test_moderate(self):
        assert determine_evidence_level(5) == "Moderate Evidence"
        assert determine_evidence_level(9) == "Moderate Evidence"

    def test_strong(self):
        assert determine_evidence_level(10) == "Strong Evidence"
        assert determine_evidence_level(50) == "Strong Evidence"


class TestStudentScenarios:
    """Test manual scenarios using the weighted scoring engine."""

    def test_student_a_data_science_high(self, student_a_courses, build_profile):
        """Student A should score high for Data Science."""
        profile = build_profile(1, student_a_courses)
        scores = score_all_specializations(profile, SPECIALIZATION_WEIGHTS)

        ds_score = next(s for s in scores if s.specialization_name == "Data Science")
        # Student A has Statistics 88, Programming 84, Database 80, Mathematics 76
        # These are all Data Science areas — should score well
        assert ds_score.academic_fit > 70

    def test_student_b_cyber_security_high(self, student_b_courses, build_profile):
        """Student B should score high for Cyber Security."""
        profile = build_profile(2, student_b_courses)
        scores = score_all_specializations(profile, SPECIALIZATION_WEIGHTS)

        cs_score = next(s for s in scores if s.specialization_name == "Cyber Security")
        assert cs_score.academic_fit > 75

    def test_student_e_limited_evidence(self, student_e_courses, build_profile):
        """Student E should have Limited Evidence."""
        profile = build_profile(5, student_e_courses, year=1, semester=1)
        scores = score_all_specializations(profile, SPECIALIZATION_WEIGHTS)

        for score in scores:
            assert score.evidence_level == "Limited Evidence"
