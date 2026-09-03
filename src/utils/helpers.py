"""
Shared utility helpers.
"""

from pathlib import Path
from typing import Any, Dict, List


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def safe_round(value: Any, decimals: int = 2) -> float:
    """Safely round a value, handling None and non-numeric types."""
    try:
        return round(float(value), decimals)
    except (TypeError, ValueError):
        return 0.0


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a value as a percentage string."""
    return f"{value:.{decimals}f}%"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis if it exceeds max_length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
