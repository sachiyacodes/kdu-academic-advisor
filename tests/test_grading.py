"""
Tests for the grading module.

Tests every grade boundary, edge cases, and error conditions.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.academic.grading import mark_to_grade, is_passing, format_grade_display


class TestMarkToGrade:
    """Test mark to grade conversion at every boundary."""

    # Grade boundaries (section 13)
    @pytest.mark.parametrize("mark, expected_grade, expected_gp", [
        (100, "A+", 4.0),
        (95, "A+", 4.0),
        (90, "A+", 4.0),
        (89, "A", 4.0),
        (87, "A", 4.0),
        (85, "A", 4.0),
        (84, "A-", 3.7),
        (82, "A-", 3.7),
        (80, "A-", 3.7),
        (79, "B+", 3.3),
        (77, "B+", 3.3),
        (75, "B+", 3.3),
        (74, "B", 3.0),
        (72, "B", 3.0),
        (70, "B", 3.0),
        (69, "B-", 2.7),
        (67, "B-", 2.7),
        (65, "B-", 2.7),
        (64, "C+", 2.3),
        (62, "C+", 2.3),
        (60, "C+", 2.3),
        (59, "C", 2.0),
        (57, "C", 2.0),
        (55, "C", 2.0),
        (54, "C-", 1.7),
        (52, "C-", 1.7),
        (50, "C-", 1.7),
        (49, "D", 1.0),
        (45, "D", 1.0),
        (40, "D", 1.0),
        (39, "F", 0.0),
        (20, "F", 0.0),
        (0, "F", 0.0),
    ])
    def test_grade_boundaries(self, mark, expected_grade, expected_gp):
        grade, gp = mark_to_grade(mark)
        assert grade == expected_grade
        assert gp == expected_gp

    def test_mark_below_zero_raises(self):
        with pytest.raises(ValueError, match="between 0 and 100"):
            mark_to_grade(-1)

    def test_mark_above_100_raises(self):
        with pytest.raises(ValueError, match="between 0 and 100"):
            mark_to_grade(101)

    def test_decimal_mark(self):
        grade, gp = mark_to_grade(89.5)
        assert grade == "A+"  # 89.5 rounds to 90
        assert gp == 4.0

    def test_decimal_at_boundary(self):
        grade, gp = mark_to_grade(39.5)
        assert grade == "D"  # 39.5 rounds to 40
        assert gp == 1.0


class TestIsPassing:
    def test_passing_mark(self):
        assert is_passing(40) is True

    def test_failing_mark(self):
        assert is_passing(39) is False

    def test_boundary(self):
        assert is_passing(40) is True
        assert is_passing(39.4) is False  # rounds to 39

    def test_high_mark(self):
        assert is_passing(100) is True

    def test_zero(self):
        assert is_passing(0) is False


class TestFormatGradeDisplay:
    def test_format(self):
        result = format_grade_display(85.0)
        assert result == "85.0 (A)"

    def test_format_failing(self):
        result = format_grade_display(30.0)
        assert result == "30.0 (F)"
