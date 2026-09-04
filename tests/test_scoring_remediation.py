"""
Tests for scoring remediation and sensitivity analysis.
Verifies calibrated_fit credibility shrinkage and sensitivity curves.
"""
import pytest
from src.ai.weighted_scoring import score_all_specializations
from src.ai.recommendation_engine import calculate_sensitivity_analysis
from src.models.schemas import AcademicProfile, StudentCourse, SubjectPerformance
from src.config.settings import SPECIALIZATION_WEIGHTS


class TestScoringRemediation:
    def test_calibrated_fit_shrinks_single_course(self):
        """
        A student with only 1 course (mark 100) should have academic_fit = 100,
        but calibrated_fit should be shrunk towards prior mean (65.0) because of sparse evidence.
        """
        perfs = {
            "Programming": SubjectPerformance("Programming", 100.0, 1, 3),
        }
        course = StudentCourse(1, 1, "CS101", "Intro to CS", 3, "Programming", 100.0, "A+", 4.0, "completed")
        profile = AcademicProfile(
            student_id=1,
            degree="Software Engineering",
            year=1,
            semester=1,
            completed_courses=[course],
            subject_performances=perfs,
            completed_course_count=1,
        )

        scores = score_all_specializations(profile, SPECIALIZATION_WEIGHTS)
        se_score = next(s for s in scores if s.specialization_name == "Software Engineering")

        assert se_score.academic_fit == pytest.approx(100.0, abs=0.1)
        # With 1 course out of 10 for strong evidence, credibility = 0.1, so calibrated fit ~ 68.5
        assert se_score.calibrated_fit < 80.0
        assert se_score.confidence_level == "Preliminary / Limited"

    def test_sensitivity_analysis_curve_generation(self):
        """Sensitivity analysis should return weight points and stability percentage."""
        perfs = {
            "Programming": SubjectPerformance("Programming", 90.0, 2, 6),
            "Software Engineering": SubjectPerformance("Software Engineering", 85.0, 1, 3),
        }
        course1 = StudentCourse(1, 1, "CS101", "Prog", 3, "Programming", 90.0, "A+", 4.0, "completed")
        course2 = StudentCourse(1, 2, "SE101", "SE", 3, "Software Engineering", 85.0, "A", 4.0, "completed")
        profile = AcademicProfile(
            student_id=1,
            degree="Software Engineering",
            year=2,
            semester=1,
            completed_courses=[course1, course2],
            subject_performances=perfs,
            completed_course_count=2,
        )

        res = calculate_sensitivity_analysis(profile, ["Programming", "Software Engineering"])
        assert len(res["academic_weights"]) == 11
        assert "Software Engineering" in res["trajectories"]
        assert 0.0 <= res["stability_percentage"] <= 100.0
