"""
CSV -> SQLite Seed Script (FIX-1)

This script reads all CSV files from data/ (the single source of truth for
static/configuration data) and populates the SQLite database.

Run this once at setup, and re-run whenever CSVs change:
    python scripts/seed_database.py

The running Streamlit application reads/writes ONLY through SQLite — it never
reads the CSVs directly at runtime.
"""

import csv
import os
import sqlite3
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"
DB_DIR = PROJECT_ROOT / "database"
DB_PATH = DB_DIR / "academic.db"


def read_csv(filename: str):
    """Read a CSV file and return list of dicts."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"  WARNING: {filename} not found, skipping.")
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def create_schema(conn: sqlite3.Connection) -> None:
    """Create all database tables with constraints."""
    conn.executescript("""
        -- Subject areas (canonical taxonomy §9)
        CREATE TABLE IF NOT EXISTS subject_areas (
            subject_area_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );

        -- Degree programs
        CREATE TABLE IF NOT EXISTS degrees (
            degree_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );

        -- Courses
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            course_code TEXT NOT NULL UNIQUE,
            course_name TEXT NOT NULL,
            degree TEXT NOT NULL,
            year INTEGER NOT NULL CHECK(year BETWEEN 1 AND 4),
            semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 2),
            credits INTEGER NOT NULL CHECK(credits >= 0),
            subject_area TEXT NOT NULL,
            FOREIGN KEY (degree) REFERENCES degrees(name),
            FOREIGN KEY (subject_area) REFERENCES subject_areas(name)
        );

        -- Specializations
        CREATE TABLE IF NOT EXISTS specializations (
            specialization_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        -- Specialization academic weights (§11)
        CREATE TABLE IF NOT EXISTS specialization_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            specialization_id INTEGER NOT NULL,
            specialization_name TEXT NOT NULL,
            subject_area TEXT NOT NULL,
            weight REAL NOT NULL CHECK(weight BETWEEN 0 AND 1),
            FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id),
            FOREIGN KEY (subject_area) REFERENCES subject_areas(name)
        );

        -- Specialization interest vectors (FIX-3)
        CREATE TABLE IF NOT EXISTS specialization_interests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            specialization_id INTEGER NOT NULL,
            specialization_name TEXT NOT NULL,
            subject_area TEXT NOT NULL,
            weight REAL NOT NULL CHECK(weight BETWEEN 0 AND 1),
            FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id),
            FOREIGN KEY (subject_area) REFERENCES subject_areas(name)
        );

        -- Prerequisites
        CREATE TABLE IF NOT EXISTS prerequisites (
            prerequisite_id INTEGER PRIMARY KEY,
            course_id INTEGER NOT NULL,
            prerequisite_course_id INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            FOREIGN KEY (prerequisite_course_id) REFERENCES courses(course_id)
        );

        -- Interests (mapped 1:1 to subject areas per §21)
        CREATE TABLE IF NOT EXISTS interests (
            interest_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            subject_area TEXT NOT NULL,
            FOREIGN KEY (subject_area) REFERENCES subject_areas(name)
        );

        -- Students (runtime data)
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            degree TEXT NOT NULL,
            year INTEGER NOT NULL CHECK(year BETWEEN 1 AND 4),
            semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 2),
            FOREIGN KEY (degree) REFERENCES degrees(name)
        );

        -- Student course records (runtime data)
        CREATE TABLE IF NOT EXISTS student_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            mark REAL NOT NULL CHECK(mark BETWEEN 0 AND 100),
            grade TEXT NOT NULL,
            grade_point REAL NOT NULL CHECK(grade_point BETWEEN 0 AND 4),
            status TEXT NOT NULL DEFAULT 'completed'
                CHECK(status IN ('completed', 'failed', 'withdrawn', 'in_progress')),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id),
            UNIQUE(student_id, course_id)
        );

        -- Student interests (runtime data)
        CREATE TABLE IF NOT EXISTS student_interests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            interest_id INTEGER NOT NULL,
            intensity REAL DEFAULT 3.0,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (interest_id) REFERENCES interests(interest_id),
            UNIQUE(student_id, interest_id)
        );

        -- Recommendation feedback (runtime data)
        CREATE TABLE IF NOT EXISTS student_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            specialization_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );
    """)


def seed_table(conn: sqlite3.Connection, table_name: str, csv_filename: str,
               columns: list, clear: bool = True) -> int:
    """Seed a table from a CSV file. Returns number of rows inserted."""
    rows = read_csv(csv_filename)
    if not rows:
        return 0

    if clear:
        conn.execute(f"DELETE FROM {table_name}")

    placeholders = ", ".join(["?"] * len(columns))
    col_names = ", ".join(columns)
    query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"

    count = 0
    for row in rows:
        values = tuple(row.get(col, None) for col in columns)
        try:
            conn.execute(query, values)
            count += 1
        except sqlite3.IntegrityError as e:
            print(f"  WARNING: Skipping row in {csv_filename}: {e}")
            print(f"    Row: {row}")

    return count


def validate_weights(conn: sqlite3.Connection) -> bool:
    """Validate that each specialization's weights sum to approximately 1.0."""
    cursor = conn.execute("""
        SELECT specialization_name, SUM(weight) as total_weight
        FROM specialization_weights
        GROUP BY specialization_name
    """)
    all_valid = True
    for row in cursor.fetchall():
        name, total = row[0], row[1]
        if abs(total - 1.0) > 0.001:
            print(f"  ERROR: {name} weights sum to {total:.4f}, expected 1.0000")
            all_valid = False
        else:
            print(f"  [OK] {name}: weights sum to {total:.4f}")

    # Also validate interest vectors
    cursor = conn.execute("""
        SELECT specialization_name, SUM(weight) as total_weight
        FROM specialization_interests
        GROUP BY specialization_name
    """)
    for row in cursor.fetchall():
        name, total = row[0], row[1]
        if abs(total - 1.0) > 0.001:
            print(f"  ERROR: {name} interest weights sum to {total:.4f}, expected 1.0000")
            all_valid = False
        else:
            print(f"  [OK] {name}: interest weights sum to {total:.4f}")

    return all_valid


def validate_subject_areas(conn: sqlite3.Connection) -> bool:
    """Validate all subject areas used in data match the canonical taxonomy."""
    valid_areas = {row[0] for row in conn.execute("SELECT name FROM subject_areas").fetchall()}

    all_valid = True

    # Check courses
    course_areas = {
        row[0] for row in conn.execute(
            "SELECT DISTINCT subject_area FROM courses"
        ).fetchall()
    }
    invalid = course_areas - valid_areas
    if invalid:
        print(f"  ERROR: Invalid subject areas in courses: {invalid}")
        all_valid = False

    # Check weights
    weight_areas = {
        row[0] for row in conn.execute(
            "SELECT DISTINCT subject_area FROM specialization_weights"
        ).fetchall()
    }
    invalid = weight_areas - valid_areas
    if invalid:
        print(f"  ERROR: Invalid subject areas in specialization_weights: {invalid}")
        all_valid = False

    # Check interest vectors
    interest_areas = {
        row[0] for row in conn.execute(
            "SELECT DISTINCT subject_area FROM specialization_interests"
        ).fetchall()
    }
    invalid = interest_areas - valid_areas
    if invalid:
        print(f"  ERROR: Invalid subject areas in specialization_interests: {invalid}")
        all_valid = False

    if all_valid:
        print("  [OK] All subject areas are valid")

    return all_valid


def main() -> None:
    """Main seed function: reads CSVs -> creates/populates SQLite."""
    print("=" * 60)
    print("CSV -> SQLite Seed Script")
    print("=" * 60)

    # Ensure database directory exists
    DB_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing database for clean seed
    if DB_PATH.exists():
        os.remove(DB_PATH)
        print(f"Removed existing database: {DB_PATH}")

    # Connect and create schema
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    print("\n1. Creating schema...")
    create_schema(conn)
    print("   [OK] Schema created")

    print("\n2. Seeding tables from CSV files...")

    # Seed in dependency order
    count = seed_table(conn, "subject_areas", "subject_areas.csv",
                       ["subject_area_id", "name"])
    print(f"   [OK] subject_areas: {count} rows")

    count = seed_table(conn, "degrees", "degrees.csv",
                       ["degree_id", "name"])
    print(f"   [OK] degrees: {count} rows")

    count = seed_table(conn, "courses", "courses.csv",
                       ["course_id", "course_code", "course_name", "degree",
                        "year", "semester", "credits", "subject_area"])
    print(f"   [OK] courses: {count} rows")

    count = seed_table(conn, "specializations", "specializations.csv",
                       ["specialization_id", "name", "description"])
    print(f"   [OK] specializations: {count} rows")

    count = seed_table(conn, "specialization_weights", "specialization_weights.csv",
                       ["specialization_id", "specialization_name",
                        "subject_area", "weight"])
    print(f"   [OK] specialization_weights: {count} rows")

    count = seed_table(conn, "specialization_interests", "specialization_interests.csv",
                       ["specialization_id", "specialization_name",
                        "subject_area", "weight"])
    print(f"   [OK] specialization_interests: {count} rows")

    count = seed_table(conn, "prerequisites", "prerequisites.csv",
                       ["prerequisite_id", "course_id", "prerequisite_course_id"])
    print(f"   [OK] prerequisites: {count} rows")

    count = seed_table(conn, "interests", "interests.csv",
                       ["interest_id", "name", "subject_area"])
    print(f"   [OK] interests: {count} rows")

    conn.commit()

    print("\n3. Validating specialization weights (§11)...")
    weights_valid = validate_weights(conn)

    print("\n4. Validating subject area taxonomy (§9)...")
    areas_valid = validate_subject_areas(conn)

    conn.close()

    print("\n" + "=" * 60)
    if weights_valid and areas_valid:
        print("[OK] Database seeded successfully!")
        print(f"  Database: {DB_PATH}")
    else:
        print("[!!] Database seeded with validation warnings!")
        print("  Review the errors above before proceeding.")
    print("=" * 60)


if __name__ == "__main__":
    main()
