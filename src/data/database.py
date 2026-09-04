"""
SQLite database access layer.

Per FIX-1 architecture: CSV files under data/ are the single source of truth
for all static/configuration data. SQLite is populated via scripts/seed_database.py
and is the ONLY thing the running application queries against.

All queries use parameterized statements to prevent SQL injection (§40).
"""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.config.settings import DATABASE_PATH


def get_db_path() -> str:
    """Get the absolute path to the database file."""
    # Resolve relative to project root
    project_root = Path(__file__).parent.parent.parent
    return str(project_root / DATABASE_PATH)


@contextmanager
def get_connection():
    """Context manager for database connections with foreign key enforcement."""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Database not found at {db_path}. "
            "Run 'python scripts/seed_database.py' first."
        )
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute a query and return all results as list of dicts."""
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def fetch_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """Execute a query and return one result as a dict, or None."""
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None


def execute(query: str, params: tuple = ()) -> int:
    """Execute a write query and return the lastrowid."""
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        return cursor.lastrowid


def execute_many(query: str, params_list: List[tuple]) -> None:
    """Execute a write query for many parameter sets."""
    with get_connection() as conn:
        conn.executemany(query, params_list)


# =============================================================================
# Domain-specific query functions
# =============================================================================

def get_all_courses(degree: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all courses, optionally filtered by degree."""
    if degree:
        return fetch_all(
            "SELECT * FROM courses WHERE degree = ? ORDER BY year, semester, course_code",
            (degree,),
        )
    return fetch_all("SELECT * FROM courses ORDER BY year, semester, course_code")


def get_course_by_id(course_id: int) -> Optional[Dict[str, Any]]:
    """Get a single course by ID."""
    return fetch_one("SELECT * FROM courses WHERE course_id = ?", (course_id,))


def get_prerequisites_for_course(course_id: int) -> List[Dict[str, Any]]:
    """Get all prerequisite courses for a given course."""
    return fetch_all(
        """
        SELECT c.* FROM courses c
        INNER JOIN prerequisites p ON c.course_id = p.prerequisite_course_id
        WHERE p.course_id = ?
        """,
        (course_id,),
    )


def get_all_prerequisites() -> List[Dict[str, Any]]:
    """Get all prerequisite relationships."""
    return fetch_all(
        """
        SELECT p.course_id, p.prerequisite_course_id,
               c1.course_code as course_code, c1.course_name as course_name,
               c2.course_code as prereq_code, c2.course_name as prereq_name
        FROM prerequisites p
        JOIN courses c1 ON p.course_id = c1.course_id
        JOIN courses c2 ON p.prerequisite_course_id = c2.course_id
        """
    )


def get_all_specializations() -> List[Dict[str, Any]]:
    """Get all specializations."""
    return fetch_all("SELECT * FROM specializations ORDER BY specialization_id")


def get_specialization_weights(specialization_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get specialization weights, optionally for a specific specialization."""
    if specialization_id:
        return fetch_all(
            "SELECT * FROM specialization_weights WHERE specialization_id = ?",
            (specialization_id,),
        )
    return fetch_all("SELECT * FROM specialization_weights")


def get_specialization_interests(specialization_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Get specialization interest vectors, optionally for a specific specialization."""
    if specialization_id:
        return fetch_all(
            "SELECT * FROM specialization_interests WHERE specialization_id = ?",
            (specialization_id,),
        )
    return fetch_all("SELECT * FROM specialization_interests")


def get_all_interests() -> List[Dict[str, Any]]:
    """Get all interest options (mapped 1:1 to subject areas)."""
    return fetch_all("SELECT * FROM interests ORDER BY interest_id")


def get_all_subject_areas() -> List[Dict[str, Any]]:
    """Get all subject areas from the canonical taxonomy."""
    return fetch_all("SELECT * FROM subject_areas ORDER BY subject_area_id")


def get_all_degrees() -> List[Dict[str, Any]]:
    """Get all degree programs."""
    return fetch_all("SELECT * FROM degrees ORDER BY degree_id")


# =============================================================================
# Student data operations (runtime read/write through SQLite only)
# =============================================================================

def save_student(degree: str, year: int, semester: int) -> int:
    """Save or update a student record. Returns student_id."""
    existing = fetch_one("SELECT student_id FROM students LIMIT 1")
    if existing:
        execute(
            "UPDATE students SET degree = ?, year = ?, semester = ? WHERE student_id = ?",
            (degree, year, semester, existing["student_id"]),
        )
        return existing["student_id"]
    return execute(
        "INSERT INTO students (degree, year, semester) VALUES (?, ?, ?)",
        (degree, year, semester),
    )


def get_student() -> Optional[Dict[str, Any]]:
    """Get the current student record (single-user prototype)."""
    return fetch_one("SELECT * FROM students LIMIT 1")


def save_student_course(student_id: int, course_id: int, mark: float,
                        grade: str, grade_point: float, status: str) -> int:
    """Save a student-course record. Updates if already exists."""
    existing = fetch_one(
        "SELECT id FROM student_courses WHERE student_id = ? AND course_id = ?",
        (student_id, course_id),
    )
    if existing:
        execute(
            """UPDATE student_courses
               SET mark = ?, grade = ?, grade_point = ?, status = ?
               WHERE student_id = ? AND course_id = ?""",
            (mark, grade, grade_point, status, student_id, course_id),
        )
        return existing["id"]
    return execute(
        """INSERT INTO student_courses (student_id, course_id, mark, grade, grade_point, status)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (student_id, course_id, mark, grade, grade_point, status),
    )


def get_student_courses(student_id: int) -> List[Dict[str, Any]]:
    """Get all course records for a student, joined with course details."""
    return fetch_all(
        """
        SELECT sc.*, c.course_code, c.course_name, c.degree, c.year, c.semester,
               c.credits, c.subject_area
        FROM student_courses sc
        INNER JOIN courses c ON sc.course_id = c.course_id
        WHERE sc.student_id = ?
        ORDER BY c.year, c.semester, c.course_code
        """,
        (student_id,),
    )


def delete_student_course(student_id: int, course_id: int) -> None:
    """Delete a student-course record."""
    execute(
        "DELETE FROM student_courses WHERE student_id = ? AND course_id = ?",
        (student_id, course_id),
    )


def clear_student_data() -> None:
    """Clear all student data (reset for new student)."""
    with get_connection() as conn:
        conn.execute("DELETE FROM student_interests")
        conn.execute("DELETE FROM student_courses")
        conn.execute("DELETE FROM students")


def save_student_interests(student_id: int, interest_ids: List[int]) -> None:
    """Save selected interests for a student. Replaces existing selections."""
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM student_interests WHERE student_id = ?",
            (student_id,),
        )
        for interest_id in interest_ids:
            conn.execute(
                "INSERT INTO student_interests (student_id, interest_id) VALUES (?, ?)",
                (student_id, interest_id),
            )


def get_student_interests(student_id: int) -> List[Dict[str, Any]]:
    """Get selected interests for a student, joined with interest details."""
    return fetch_all(
        """
        SELECT i.* FROM interests i
        INNER JOIN student_interests si ON i.interest_id = si.interest_id
        WHERE si.student_id = ?
        ORDER BY i.interest_id
        """,
        (student_id,),
    )
