"""
Tests for interest matching remediation.
Verifies continuous 1-5 Likert intensity and cosine breadth non-dilution.
"""
import pytest
from src.ai.interest_matching import (
    build_student_interest_vector,
    calculate_interest_score,
)
from src.config.settings import SPECIALIZATION_INTEREST_VECTORS


class TestInterestRemediation:
    def test_continuous_intensity_vector_construction(self):
        """Dict of {area: intensity 1-5} should scale to [0.2, 1.0]."""
        interests = {"Programming": 5.0, "Database": 2.5}
        vec = build_student_interest_vector(interests)
        assert len(vec) == 13
        from src.config.settings import SUBJECT_AREA_ORDER
        prog_idx = SUBJECT_AREA_ORDER.index("Programming")
        db_idx = SUBJECT_AREA_ORDER.index("Database")
        assert vec[prog_idx] == 1.0
        assert vec[db_idx] == pytest.approx(0.5, abs=0.01)

    def test_multi_interest_does_not_severely_dilute_matching_spec(self):
        """
        Selecting multiple related interests should maintain high score
        thanks to coverage boost.
        """
        ds_weights = SPECIALIZATION_INTEREST_VECTORS["Data Science"]
        single_interest = ["Statistics"]
        broad_interests = ["Statistics", "Data Analysis", "Database", "Mathematics"]

        score_single, _ = calculate_interest_score(single_interest, ds_weights)
        score_broad, _ = calculate_interest_score(broad_interests, ds_weights)

        # Broad interest should NOT be penalized relative to a single interest
        assert score_broad >= score_single * 0.90
        assert score_broad > 50.0
