"""
Integration tests — full pipeline from student input to recommendations.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.academic.profile import build_academic_profile, build_student_courses
from src.academic.grading import mark_to_grade
from src.ai.recommendation_engine import generate_recommendations
from src.ai.explanations import generate_all_explanations
from src.config.settings import SubjectArea, CourseStatus


class TestFullPipeline:
    """End-to-end integration tests through the recommendation pipeline."""

    def test_student_a_full_pipeline(self, student_a_courses, student_a_interests, build_profile):
        """Full pipeline for Student A: profile -> scoring -> recommendations -> explanations."""
        profile = build_profile(1, student_a_courses)

        # Generate recommendations
        scores = generate_recommendations(profile, student_a_interests)

        # Generate explanations
        explanations = generate_all_explanations(scores)

        # Assertions
        assert len(scores) == 6
        assert all(s.rank > 0 for s in scores)
        assert all(s.final_score >= 0 for s in scores)
        assert len(explanations) == 6

        # Data Science should be top
        assert "Data Science" in [s.specialization_name for s in scores[:2]]

        # Every explanation should have content
        for spec_name, exp in explanations.items():
            assert exp.summary != ""
            assert exp.evidence_note != ""

    def test_no_interests_pipeline(self, student_a_courses, build_profile):
        """Pipeline works with no interests selected."""
        profile = build_profile(1, student_a_courses)
        scores = generate_recommendations(profile, [])

        # Should still produce rankings based on academic fit alone
        assert len(scores) == 6
        for s in scores:
            assert s.interest_alignment == 0.0
            assert s.final_score == pytest.approx(s.academic_fit * 0.70, abs=0.01)

    def test_single_course_pipeline(self, student_e_courses, build_profile):
        """Pipeline works with just one course."""
        profile = build_profile(5, student_e_courses, year=1, semester=1)
        scores = generate_recommendations(profile, [])

        assert len(scores) == 6
        for s in scores:
            assert s.evidence_level == "Limited Evidence"

    def test_score_consistency(self, student_b_courses, student_b_interests, build_profile):
        """Running the pipeline twice should give identical results."""
        profile = build_profile(2, student_b_courses)
        scores1 = generate_recommendations(profile, student_b_interests)
        scores2 = generate_recommendations(profile, student_b_interests)

        for s1, s2 in zip(scores1, scores2):
            assert s1.final_score == s2.final_score
            assert s1.academic_fit == s2.academic_fit
            assert s1.interest_alignment == s2.interest_alignment

    def test_all_scenarios_produce_valid_output(
        self,
        student_a_courses, student_a_interests,
        student_b_courses, student_b_interests,
        student_c_courses, student_c_interests,
        student_d_courses, student_d_interests,
        student_e_courses, student_e_interests,
        build_profile,
    ):
        """All 5 manual scenarios produce valid, non-error output."""
        scenarios = [
            (1, student_a_courses, student_a_interests),
            (2, student_b_courses, student_b_interests),
            (3, student_c_courses, student_c_interests),
            (4, student_d_courses, student_d_interests),
            (5, student_e_courses, student_e_interests),
        ]

        for sid, courses, interests in scenarios:
            year = 1 if sid == 5 else 2
            profile = build_profile(sid, courses, year=year)
            scores = generate_recommendations(profile, interests)

            assert len(scores) == 6, f"Student {sid}: expected 6 specializations"
            assert all(0 <= s.final_score <= 100 for s in scores), \
                f"Student {sid}: score out of range"
            assert sorted([s.rank for s in scores]) == [1, 2, 3, 4, 5, 6], \
                f"Student {sid}: invalid ranking"
