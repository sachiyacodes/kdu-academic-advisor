"""
Tests for the GPA calculation module.

Tests normal calculation, failed courses, withdrawn, repeated,
zero-credit, and edge cases.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.academic.gpa import calculate_gpa, calculate_subject_gpa, get_gpa_classification


class TestCalculateGPA:
    def test_basic_gpa(self):
        records = [
            {"grade_point": 4.0, "credits": 3, "status": "completed"},
            {"grade_point": 3.0, "credits": 4, "status": "completed"},
        ]
        gpa, earned, attempted = calculate_gpa(records)
        # (4.0*3 + 3.0*4) / (3+4) = 24/7 = 3.43
        assert gpa == pytest.approx(3.43, abs=0.01)
        assert earned == 7
        assert attempted == 7

    def test_gpa_with_failed_course(self):
        records = [
            {"grade_point": 4.0, "credits": 3, "status": "completed"},
            {"grade_point": 0.0, "credits": 3, "status": "failed"},
        ]
        gpa, earned, attempted = calculate_gpa(records)
        # (4.0*3 + 0.0*3) / 6 = 12/6 = 2.0
        assert gpa == pytest.approx(2.0, abs=0.01)
        assert earned == 3  # Only completed counted as earned
        assert attempted == 6

    def test_withdrawn_excluded(self):
        records = [
            {"grade_point": 4.0, "credits": 3, "status": "completed"},
            {"grade_point": 1.0, "credits": 3, "status": "withdrawn"},
        ]
        gpa, earned, attempted = calculate_gpa(records)
        assert gpa == pytest.approx(4.0, abs=0.01)
        assert earned == 3
        assert attempted == 3

    def test_in_progress_excluded(self):
        records = [
            {"grade_point": 3.0, "credits": 4, "status": "completed"},
            {"grade_point": 0.0, "credits": 3, "status": "in_progress"},
        ]
        gpa, earned, attempted = calculate_gpa(records)
        assert gpa == pytest.approx(3.0, abs=0.01)
        assert attempted == 4

    def test_zero_credit_excluded(self):
        records = [
            {"grade_point": 4.0, "credits": 3, "status": "completed"},
            {"grade_point": 4.0, "credits": 0, "status": "completed"},
        ]
        gpa, earned, attempted = calculate_gpa(records)
        assert gpa == pytest.approx(4.0, abs=0.01)
        assert attempted == 3

    def test_empty_records(self):
        gpa, earned, attempted = calculate_gpa([])
        assert gpa == 0.0
        assert earned == 0
        assert attempted == 0

    def test_all_failed(self):
        records = [
            {"grade_point": 0.0, "credits": 3, "status": "failed"},
            {"grade_point": 0.0, "credits": 4, "status": "failed"},
        ]
        gpa, earned, attempted = calculate_gpa(records)
        assert gpa == 0.0
        assert earned == 0
        assert attempted == 7

    def test_ngpa_course_excluded_from_gpa(self):
        """NGPA courses must NOT affect GPA quality points, but count towards earned credits."""
        records = [
            {"grade_point": 4.0, "credits": 3, "status": "completed", "course_type": "Core"},
            {"grade_point": 2.0, "credits": 2, "status": "completed", "course_type": "NGPA"},
        ]
        gpa, earned, attempted = calculate_gpa(records)
        # Only Core course counts in GPA: 4.0 * 3 / 3 = 4.0
        assert gpa == 4.0
        assert attempted == 3
        # Both count in total credits earned: 3 + 2 = 5
        assert earned == 5

    def test_ngpa_only_courses(self):
        """Student with only NGPA courses has 0.0 GPA with credits earned counted."""
        records = [
            {"grade_point": 3.0, "credits": 2, "status": "completed", "course_type": "NGPA"},
        ]
        gpa, earned, attempted = calculate_gpa(records)
        assert gpa == 0.0
        assert attempted == 0
        assert earned == 2


class TestGPAClassification:
    def test_first_class(self):
        assert get_gpa_classification(3.9) == "First Class Honours"

    def test_second_upper(self):
        assert get_gpa_classification(3.5) == "Second Class Upper"

    def test_second_lower(self):
        assert get_gpa_classification(2.8) == "Second Class Lower"

    def test_pass(self):
        assert get_gpa_classification(2.2) == "Pass"

    def test_conditional(self):
        assert get_gpa_classification(0.5) == "Conditional"

    def test_zero(self):
        assert get_gpa_classification(0.0) == "Not Available"
