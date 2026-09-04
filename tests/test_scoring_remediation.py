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

    def test_detect_academic_stage_respects_declared_year_and_sem(self):
        """When student selects Year 4 Semester 1 with 0 completed credits, stage must be Year 4 - Semester 1."""
        from src.academic.profile import detect_academic_stage
        stage = detect_academic_stage(year=4, semester=1, completed_credits=0)
        assert stage == "Year 4 - Semester 1"

        stage_with_credits = detect_academic_stage(year=2, semester=1, completed_credits=30)
        assert stage_with_credits == "Year 2 - Semester 1"

    def test_compute_completed_steps_progress(self):
        """Step tracker must accurately and uniformly compute progress."""
        from src.ui.components import compute_completed_steps
        assert compute_completed_steps(None) == []

        student = {"student_id": 999}
        assert compute_completed_steps(student, courses=[], interests=[]) == [1]
        assert compute_completed_steps(student, courses=[{"id": 1}], interests=[]) == [1, 2, 4, 5, 6]
        assert compute_completed_steps(student, courses=[{"id": 1}], interests=[{"interest_id": 1}]) == [1, 2, 3, 4, 5, 6]

    def test_specialization_chart_reverses_yaxis(self):
        """Horizontal comparison bar chart must reverse yaxis so #1 rank is displayed at top."""
        from src.ui.components import render_specialization_comparison_chart
        from src.models.schemas import SpecializationScore
        s1 = SpecializationScore(specialization_name="SE", academic_fit=80, final_score=80)
        s2 = SpecializationScore(specialization_name="DS", academic_fit=70, final_score=70)
        fig = render_specialization_comparison_chart([s1, s2])
        assert fig.layout.yaxis.autorange == "reversed"

    def test_ml_zero_mark_handling(self):
        """ML prediction should accept 0.0 marks as valid completed marks and not drop them."""
        from ml.predict import predict_specialization
        res = predict_specialization({"Programming": 0.0})
        assert res is not None
        assert isinstance(res[0], str)

    def test_missing_prereq_safe_string_formatting(self):
        """Rule engine missing prereq formatting should never yield None items."""
        from src.ai.rule_engine import categorize_course
        from src.models.schemas import AcademicProfile
        p = AcademicProfile(student_id=1, degree="IT", year=2, semester=1)
        c = {"course_id": 99, "course_code": "IT2200", "course_name": "Adv Prog", "year": 2, "semester": 2, "credits": 3, "subject_area": "Programming"}
        # Prerequisite with None prereq_name
        prereqs = [{"course_id": 99, "prerequisite_course_id": 50, "prereq_name": None, "prereq_code": "IT1101"}]
        rec = categorize_course(c, p, prereqs, {"Programming"})
        assert "IT1101" in rec.missing_prerequisites
        assert None not in rec.missing_prerequisites

