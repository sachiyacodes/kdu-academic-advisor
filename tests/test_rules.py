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
