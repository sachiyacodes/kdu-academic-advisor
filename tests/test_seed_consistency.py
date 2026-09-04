"""
Tests for CSV -> SQLite seed consistency (FIX-1).

Verifies that the seeded SQLite database matches the CSV source-of-truth files.
"""

import csv
import sqlite3
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import SubjectArea, SUBJECT_AREA_ORDER

DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = PROJECT_ROOT / "database" / "academic.db"


@pytest.fixture
def db_conn():
    """Get a database connection for testing."""
    if not DB_PATH.exists():
        pytest.skip("Database not found. Run seed_database.py first.")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def read_csv_file(filename):
    """Read a CSV file from data/."""
    filepath = DATA_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestSeedConsistency:
    """Verify SQLite data matches CSV source-of-truth files."""

    def test_subject_areas_count(self, db_conn):
        """Subject areas in DB should match CSV."""
        csv_rows = read_csv_file("subject_areas.csv")
        db_rows = db_conn.execute("SELECT * FROM subject_areas").fetchall()
        assert len(db_rows) == len(csv_rows) == 13

    def test_subject_area_names_match(self, db_conn):
        """Every subject area name in DB should match the canonical taxonomy."""
        db_names = {
            row["name"]
            for row in db_conn.execute("SELECT name FROM subject_areas").fetchall()
        }
        canonical = set(SUBJECT_AREA_ORDER)
        assert db_names == canonical

    def test_degrees_count(self, db_conn):
        csv_rows = read_csv_file("degrees.csv")
        db_rows = db_conn.execute("SELECT * FROM degrees").fetchall()
        assert len(db_rows) == len(csv_rows)

    def test_courses_count(self, db_conn):
        csv_rows = read_csv_file("courses.csv")
        db_rows = db_conn.execute("SELECT * FROM courses").fetchall()
        assert len(db_rows) == len(csv_rows)

    def test_specializations_count(self, db_conn):
        csv_rows = read_csv_file("specializations.csv")
        db_rows = db_conn.execute("SELECT * FROM specializations").fetchall()
        assert len(db_rows) == len(csv_rows) == 6

    def test_specialization_weights_count(self, db_conn):
        csv_rows = read_csv_file("specialization_weights.csv")
        db_rows = db_conn.execute("SELECT * FROM specialization_weights").fetchall()
        assert len(db_rows) == len(csv_rows)

    def test_specialization_interests_count(self, db_conn):
        csv_rows = read_csv_file("specialization_interests.csv")
        db_rows = db_conn.execute("SELECT * FROM specialization_interests").fetchall()
        assert len(db_rows) == len(csv_rows)

    def test_prerequisites_count(self, db_conn):
        csv_rows = read_csv_file("prerequisites.csv")
        db_rows = db_conn.execute("SELECT * FROM prerequisites").fetchall()
        assert len(db_rows) == len(csv_rows)

    def test_interests_count(self, db_conn):
        csv_rows = read_csv_file("interests.csv")
        db_rows = db_conn.execute("SELECT * FROM interests").fetchall()
        assert len(db_rows) == len(csv_rows) == 13

    def test_weight_sums(self, db_conn):
        """Every specialization's weights should sum to 1.0."""
        cursor = db_conn.execute("""
            SELECT specialization_name, SUM(weight) as total
            FROM specialization_weights
            GROUP BY specialization_name
        """)
        for row in cursor.fetchall():
            assert abs(row["total"] - 1.0) < 0.001, \
                f"{row['specialization_name']} weights sum to {row['total']}"

    def test_interest_weight_sums(self, db_conn):
        """Every specialization's interest weights should sum to 1.0."""
        cursor = db_conn.execute("""
            SELECT specialization_name, SUM(weight) as total
            FROM specialization_interests
            GROUP BY specialization_name
        """)
        for row in cursor.fetchall():
            assert abs(row["total"] - 1.0) < 0.001, \
                f"{row['specialization_name']} interest weights sum to {row['total']}"

    def test_course_subject_areas_valid(self, db_conn):
        """All course subject areas should be in the canonical taxonomy."""
        valid_areas = set(SUBJECT_AREA_ORDER)
        cursor = db_conn.execute("SELECT DISTINCT subject_area FROM courses")
        for row in cursor.fetchall():
            assert row["subject_area"] in valid_areas, \
                f"Invalid subject area in courses: {row['subject_area']}"

    def test_data_science_weights_match_proposal(self, db_conn):
        """Data Science weights must match proposal exactly (section 11)."""
        rows = db_conn.execute("""
            SELECT subject_area, weight FROM specialization_weights
            WHERE specialization_name = 'Data Science'
        """).fetchall()
        weights = {row["subject_area"]: row["weight"] for row in rows}

        assert weights["Statistics"] == pytest.approx(0.30)
        assert weights["Programming"] == pytest.approx(0.25)
        assert weights["Database"] == pytest.approx(0.20)
        assert weights["Mathematics"] == pytest.approx(0.15)
        assert weights["Other"] == pytest.approx(0.10)

    def test_clear_student_data_foreign_keys(self):
        """clear_student_data should clean up student_interests, courses, and students without FK violation."""
        from src.data import database as db
        sid = db.save_student("Software Engineering", 2, 1)
        db.save_student_course(sid, 35, 80.0, "A", 4.0, "completed")
        db.save_student_interests(sid, [1, 2])

        # Must succeed without sqlite3.IntegrityError
        db.clear_student_data()
        assert db.get_student() is None
        assert db.get_student_courses(sid) == []
        assert db.get_student_interests(sid) == []
