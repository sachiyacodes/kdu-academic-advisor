"""
Tests for the rule-based reasoning engine (AI Concept 1).

Tests prerequisite checking, stage eligibility, and course categorization.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.rule_engine import (
    check_prerequisites,
    check_stage_eligibility,
)


class TestPrerequisiteChecking:
    def test_no_prerequisites(self):
        """Course with no prerequisites should be satisfied."""
        satisfied, missing = check_prerequisites(1, {1, 2, 3}, [])
        assert satisfied is True
        assert missing == []

    def test_all_prerequisites_met(self):
        """All prerequisites completed should be satisfied."""
        prereqs = [
            {"course_id": 5, "prerequisite_course_id": 1},
            {"course_id": 5, "prerequisite_course_id": 2},
        ]
        satisfied, missing = check_prerequisites(5, {1, 2, 3}, prereqs)
        assert satisfied is True
        assert missing == []

    def test_missing_one_prerequisite(self):
        """One missing prerequisite should not be satisfied."""
        prereqs = [
            {"course_id": 5, "prerequisite_course_id": 1},
            {"course_id": 5, "prerequisite_course_id": 2},
        ]
        satisfied, missing = check_prerequisites(5, {1}, prereqs)
        assert satisfied is False
        assert len(missing) == 1
        assert missing[0]["prerequisite_course_id"] == 2

    def test_all_prerequisites_missing(self):
        """All prerequisites missing."""
        prereqs = [
            {"course_id": 5, "prerequisite_course_id": 1},
            {"course_id": 5, "prerequisite_course_id": 2},
        ]
        satisfied, missing = check_prerequisites(5, set(), prereqs)
        assert satisfied is False
        assert len(missing) == 2

    def test_unrelated_prerequisites_ignored(self):
        """Prerequisites for other courses should not affect this course."""
        prereqs = [
            {"course_id": 10, "prerequisite_course_id": 1},  # different course
        ]
        satisfied, missing = check_prerequisites(5, set(), prereqs)
        assert satisfied is True


class TestStageEligibility:
    def test_same_year_same_semester(self):
        assert check_stage_eligibility(2, 1, 2, 1) is True

    def test_higher_year(self):
        assert check_stage_eligibility(1, 2, 2, 1) is True

    def test_lower_year(self):
        assert check_stage_eligibility(3, 1, 2, 1) is False

    def test_same_year_lower_semester(self):
        assert check_stage_eligibility(2, 2, 2, 1) is False

    def test_same_year_higher_semester(self):
        assert check_stage_eligibility(2, 1, 2, 2) is True

    def test_year_4_student_year_1_course(self):
        assert check_stage_eligibility(1, 1, 4, 2) is True


class TestElectiveSynergy:
    def test_synergy_maximum_weight(self):
        """Top weighted area should give 100% synergy."""
        from src.ai.rule_engine import calculate_elective_synergy
        # Data Science: Statistics is 0.30 (max)
        score = calculate_elective_synergy("Statistics", "Data Science")
        assert score == 100.0

    def test_synergy_partial_weight(self):
        """Partial weight area should calculate proportional synergy."""
        from src.ai.rule_engine import calculate_elective_synergy
        # Data Science: Programming is 0.25 -> 0.25 / 0.30 * 100 = 83.3
        score = calculate_elective_synergy("Programming", "Data Science")
        assert score == 83.3

    def test_synergy_zero_for_unrelated(self):
        """Unrelated area should yield 0.0 synergy."""
        from src.ai.rule_engine import calculate_elective_synergy
        score = calculate_elective_synergy("Cyber Security", "Data Science")
        assert score == 0.0

    def test_synergy_invalid_spec(self):
        """Unknown specialization should yield 0.0 synergy."""
        from src.ai.rule_engine import calculate_elective_synergy
        score = calculate_elective_synergy("Programming", "Nonexistent Specialization")
        assert score == 0.0


class TestCourseCategorization:
    def test_elective_categorization_with_synergy(self):
        from src.ai.rule_engine import categorize_course
        from src.models.schemas import AcademicProfile

        profile = AcademicProfile(student_id=1, degree="Software Engineering", year=3, semester=1)
        course = {
            "course_id": 101,
            "course_code": "CS3010",
            "course_name": "Machine Learning Foundations",
            "degree": "Software Engineering",
            "year": 3,
            "semester": 1,
            "credits": 3,
            "subject_area": "Artificial Intelligence",
            "course_type": "Elective",
        }
        rec = categorize_course(
            course=course,
            profile=profile,
            all_prerequisites=[],
            specialization_subject_areas={"Artificial Intelligence"},
            top_specialization_name="Artificial Intelligence / Machine Learning",
        )
        assert rec.course.course_type == "Elective"
        assert rec.category == "Recommended Now"
        assert rec.synergy_score > 0.0
        assert rec.target_specialization == "Artificial Intelligence / Machine Learning"
        assert "Elective with" in rec.reason


class TestGraduationAuditAndCustomCourse:
    def test_graduation_credit_targets(self):
        from src.config.settings import GRADUATION_MIN_GPA_CREDITS, GRADUATION_MIN_NGPA_CREDITS
        assert GRADUATION_MIN_GPA_CREDITS == 120
        assert GRADUATION_MIN_NGPA_CREDITS == 14

    def test_recommendations_with_custom_degree_and_synergy(self):
        from src.ai.rule_engine import get_course_recommendations
        from src.models.schemas import AcademicProfile

        profile = AcademicProfile(student_id=99, degree="Custom / Other University Degree", year=3, semester=1)
        courses = [
            {
                "course_id": 901,
                "course_code": "STAT301",
                "course_name": "Advanced Statistical Inference",
                "degree": "Custom / Other University Degree",
                "year": 3,
                "semester": 1,
                "credits": 3,
                "subject_area": "Statistics",
                "course_type": "Elective",
            },
            {
                "course_id": 902,
                "course_code": "CS302",
                "course_name": "Distributed Systems",
                "degree": "Custom / Other University Degree",
                "year": 3,
                "semester": 1,
                "credits": 3,
                "subject_area": "Systems & Operating Systems",
                "course_type": "Core",
            },
        ]
        recs = get_course_recommendations(
            profile=profile,
            all_courses=courses,
            all_prerequisites=[],
            top_specialization_areas={"Statistics", "Systems & Operating Systems"},
            top_specialization_name="Data Science",
        )
        assert len(recs) == 2
        stat_rec = next(r for r in recs if r.course.course_code == "STAT301")
        assert stat_rec.course.course_type == "Elective"
        assert stat_rec.synergy_score == 100.0  # Statistics has max weight in Data Science
        assert stat_rec.target_specialization == "Data Science"

        cs_rec = next(r for r in recs if r.course.course_code == "CS302")
        assert cs_rec.course.course_type == "Core"


