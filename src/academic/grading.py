"""
Grading module — converts marks to letter grades and grade points.

Uses the prototype grading scale from §13 (NOT official KDU grading policy).
The scale is defined in src/config/settings.py and is editable configuration.

AI classification: This is standard academic arithmetic, not AI/ML.
"""

from typing import Optional, Tuple

from src.config.settings import GRADING_SCALE, MINIMUM_PASS_MARK


def mark_to_grade(mark: float) -> Tuple[str, float]:
    """
    Convert a numeric mark (0-100) to (letter_grade, grade_point).

    Args:
        mark: Numeric mark between 0 and 100.

    Returns:
        Tuple of (grade string, grade point value).

    Raises:
        ValueError: If mark is outside 0-100 range.
    """
    if mark < 0 or mark > 100:
        raise ValueError(f"Mark must be between 0 and 100, got {mark}")

    mark_rounded = round(mark)

    for min_mark, max_mark, grade, grade_point in GRADING_SCALE:
        if min_mark <= mark_rounded <= max_mark:
            return grade, grade_point

    # Fallback — should never reach here if GRADING_SCALE covers 0-100
    return "F", 0.0


def is_passing(mark: float) -> bool:
    """Check if a mark meets the minimum pass threshold."""
    return round(mark) >= MINIMUM_PASS_MARK


def get_grade_description(grade: str) -> str:
    """Get a human-readable description for a letter grade."""
    descriptions = {
        "A+": "Excellent",
        "A": "Excellent",
        "A-": "Very Good",
        "B+": "Good",
        "B": "Good",
        "B-": "Above Average",
        "C+": "Average",
        "C": "Average",
        "C-": "Below Average",
        "D": "Poor",
        "F": "Fail",
    }
    return descriptions.get(grade, "Unknown")


def format_grade_display(mark: float) -> str:
    """Format a mark for display: '85 (A)'."""
    grade, _ = mark_to_grade(mark)
    return f"{mark:.1f} ({grade})"
