"""
Tests for the interest matching engine (AI Concept 3, FIX-3).

Verifies the cosine similarity formula against the proposal's definition.
"""

import pytest
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.interest_matching import (
    build_student_interest_vector,
    build_specialization_interest_vector,
    cosine_similarity,
    calculate_interest_score,
    score_interests_all_specializations,
)
from src.config.settings import (
    SUBJECT_AREA_ORDER,
    SPECIALIZATION_INTEREST_VECTORS,
    SubjectArea,
)


class TestVectorConstruction:
    def test_student_vector_single_interest(self):
        """Single interest should activate exactly one dimension."""
        vec = build_student_interest_vector(["Programming"])
        assert vec[SUBJECT_AREA_ORDER.index("Programming")] == 1.0
        assert sum(vec) == 1.0

    def test_student_vector_multiple_interests(self):
        """Multiple interests activate multiple dimensions."""
        vec = build_student_interest_vector(["Programming", "Statistics"])
        assert vec[SUBJECT_AREA_ORDER.index("Programming")] == 1.0
        assert vec[SUBJECT_AREA_ORDER.index("Statistics")] == 1.0
        assert sum(vec) == 2.0

    def test_student_vector_no_interests(self):
        """No interests should be all zeros."""
        vec = build_student_interest_vector([])
        assert sum(vec) == 0.0
        assert len(vec) == 13

    def test_student_vector_all_interests(self):
        """All interests selected."""
        vec = build_student_interest_vector(SUBJECT_AREA_ORDER)
        assert sum(vec) == 13.0

    def test_specialization_vector_length(self):
        """Specialization vector should always be length 13."""
        for spec_name, weights in SPECIALIZATION_INTEREST_VECTORS.items():
            vec = build_specialization_interest_vector(weights)
            assert len(vec) == 13, f"{spec_name} vector has wrong length"


class TestCosineSimilarity:
    def test_identical_vectors(self):
        """Identical vectors should give similarity 1.0."""
        vec = [1.0, 0.0, 1.0, 0.0]
        assert cosine_similarity(vec, vec) == pytest.approx(1.0, abs=0.001)

    def test_orthogonal_vectors(self):
        """Orthogonal vectors should give similarity 0.0."""
        assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0, abs=0.001)

    def test_zero_vector(self):
        """Zero vector should return 0.0."""
        assert cosine_similarity([0, 0], [1, 1]) == 0.0

    def test_known_value(self):
        """Test against a known cosine similarity value."""
        a = [1.0, 2.0, 3.0]
        b = [4.0, 5.0, 6.0]
        expected = (1*4 + 2*5 + 3*6) / (math.sqrt(14) * math.sqrt(77))
        assert cosine_similarity(a, b) == pytest.approx(expected, abs=0.001)

    def test_different_length_raises(self):
        with pytest.raises(ValueError, match="same length"):
            cosine_similarity([1, 2], [1, 2, 3])


class TestInterestScore:
    def test_perfect_match(self):
        """Interest perfectly aligned with specialization."""
        interests = ["Programming"]
        spec_weights = {"Programming": 1.0}
        score, contribs = calculate_interest_score(interests, spec_weights)
        assert score == pytest.approx(100.0, abs=0.1)
        assert "Programming" in contribs

    def test_no_interests(self):
        """No interests should give 0."""
        score, contribs = calculate_interest_score([], {"Programming": 1.0})
        assert score == 0.0
        assert contribs == {}

    def test_no_overlap(self):
        """Interest in area not weighted by specialization should give low score."""
        interests = ["Cloud Computing"]
        spec_weights = {"Programming": 0.5, "Mathematics": 0.5}
        score, contribs = calculate_interest_score(interests, spec_weights)
        assert score == 0.0

    def test_partial_overlap(self):
        """Partial interest overlap."""
        interests = ["Programming", "Database"]
        spec_weights = {"Programming": 0.5, "Mathematics": 0.3, "Database": 0.2}
        score, contribs = calculate_interest_score(interests, spec_weights)
        assert score > 0
        assert "Programming" in contribs
        assert "Database" in contribs
        assert "Mathematics" not in contribs


class TestInterestScenarios:
    """Test interest matching against manual scenarios."""

    def test_student_a_data_science_interest(self, student_a_interests):
        """Student A's Data Analysis + Statistics interests should match Data Science."""
        ds_interests = SPECIALIZATION_INTEREST_VECTORS.get("Data Science", {})
        score, contribs = calculate_interest_score(student_a_interests, ds_interests)
        # Data Science has high weights for Statistics and Data Analysis
        assert score > 50

    def test_student_b_cyber_security_interest(self, student_b_interests):
        """Student B's Cyber Security + Networking interests should match Cyber Security."""
        cs_interests = SPECIALIZATION_INTEREST_VECTORS.get("Cyber Security", {})
        score, contribs = calculate_interest_score(student_b_interests, cs_interests)
        assert score > 50

    def test_student_e_no_interests(self, student_e_interests):
        """Student E has no interests — score should be 0."""
        for spec_weights in SPECIALIZATION_INTEREST_VECTORS.values():
            score, _ = calculate_interest_score(student_e_interests, spec_weights)
            assert score == 0.0
