"""
Synthetic Student Dataset Generator.

Generates 500-1000 realistic synthetic students with reproducible random seed.
Includes realistic correlations (e.g., programming strength correlating loosely
with software engineering performance) plus realistic noise.

DISCLAIMER: The dataset is synthetic, intended for demonstration and evaluation
of the prototype. Results cannot be assumed to represent real KDU students.

Documented seed value: 42 (see src/config/settings.py SYNTHETIC_SEED)
"""

import csv
import os
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import (
    DEGREE_PROGRAMS,
    GRADING_SCALE,
    MINIMUM_PASS_MARK,
    SYNTHETIC_SEED,
    SYNTHETIC_STUDENT_COUNT,
    SubjectArea,
)

DATA_DIR = PROJECT_ROOT / "data"
COURSES_FILE = DATA_DIR / "courses.csv"
OUTPUT_FILE = DATA_DIR / "synthetic_students.csv"


def load_courses():
    """Load courses from CSV."""
    courses = []
    with open(COURSES_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["course_id"] = int(row["course_id"])
            row["year"] = int(row["year"])
            row["semester"] = int(row["semester"])
            row["credits"] = int(row["credits"])
            courses.append(row)
    return courses


def get_grade(mark: float) -> tuple:
    """Convert mark to (grade, grade_point)."""
    mark_int = int(round(mark))
    for min_mark, max_mark, grade, gp in GRADING_SCALE:
        if min_mark <= mark_int <= max_mark:
            return grade, gp
    return "F", 0.0


# Student archetype base strengths per subject area (mean marks).
# These create realistic correlations between related subjects.
ARCHETYPES = {
    "data_science": {
        SubjectArea.STATISTICS.value: 82,
        SubjectArea.PROGRAMMING.value: 75,
        SubjectArea.DATABASE.value: 74,
        SubjectArea.MATHEMATICS.value: 78,
        SubjectArea.DATA_ANALYSIS.value: 80,
        SubjectArea.ARTIFICIAL_INTELLIGENCE.value: 70,
        SubjectArea.ALGORITHMS_DS.value: 68,
        SubjectArea.OTHER.value: 65,
    },
    "ai_ml": {
        SubjectArea.MATHEMATICS.value: 82,
        SubjectArea.STATISTICS.value: 76,
        SubjectArea.PROGRAMMING.value: 78,
        SubjectArea.ALGORITHMS_DS.value: 80,
        SubjectArea.ARTIFICIAL_INTELLIGENCE.value: 85,
        SubjectArea.DATA_ANALYSIS.value: 72,
        SubjectArea.OTHER.value: 62,
    },
    "cyber_security": {
        SubjectArea.CYBER_SECURITY.value: 85,
        SubjectArea.NETWORKING.value: 80,
        SubjectArea.PROGRAMMING.value: 72,
        SubjectArea.SYSTEMS_OS.value: 78,
        SubjectArea.MATHEMATICS.value: 60,
        SubjectArea.OTHER.value: 64,
    },
    "software_engineering": {
        SubjectArea.PROGRAMMING.value: 85,
        SubjectArea.SOFTWARE_ENGINEERING.value: 82,
        SubjectArea.ALGORITHMS_DS.value: 78,
        SubjectArea.DATABASE.value: 72,
        SubjectArea.SYSTEMS_OS.value: 70,
        SubjectArea.OTHER.value: 68,
    },
    "networking_cloud": {
        SubjectArea.NETWORKING.value: 83,
        SubjectArea.SYSTEMS_OS.value: 78,
        SubjectArea.CYBER_SECURITY.value: 72,
        SubjectArea.PROGRAMMING.value: 65,
        SubjectArea.CLOUD_COMPUTING.value: 80,
        SubjectArea.OTHER.value: 63,
    },
    "database_engineering": {
        SubjectArea.DATABASE.value: 84,
        SubjectArea.PROGRAMMING.value: 73,
        SubjectArea.DATA_ANALYSIS.value: 76,
        SubjectArea.MATHEMATICS.value: 70,
        SubjectArea.STATISTICS.value: 72,
        SubjectArea.SYSTEMS_OS.value: 68,
        SubjectArea.OTHER.value: 65,
    },
    "balanced": {
        # No strong preference — moderate across the board
    },
    "struggling": {
        # Below average everywhere
    },
}


def generate_mark(rng: random.Random, base_mean: float, noise_std: float = 12.0) -> float:
    """Generate a realistic mark with Gaussian noise, clamped to 0-100."""
    mark = rng.gauss(base_mean, noise_std)
    return max(0.0, min(100.0, round(mark, 1)))


def generate_student(rng: random.Random, student_id: int, courses: list) -> list:
    """Generate course records for one synthetic student."""
    # Pick a degree from available catalog curricula
    curricula_degrees = sorted(list({c["degree"] for c in courses}))
    degree = rng.choice(curricula_degrees)

    # Filter courses for this degree
    degree_courses = [c for c in courses if c["degree"] == degree]

    # Pick academic progress (how far along they are)
    max_year = rng.choices([1, 2, 3, 4], weights=[15, 30, 35, 20])[0]
    max_semester = rng.choice([1, 2])

    # Pick an archetype
    archetype_name = rng.choice(list(ARCHETYPES.keys()))
    archetype = ARCHETYPES[archetype_name]

    # Base performance level (shifts entire profile up/down)
    base_offset = rng.gauss(0, 8)

    # Default mean for subjects not in archetype
    if archetype_name == "struggling":
        default_mean = rng.gauss(48, 8)
    elif archetype_name == "balanced":
        default_mean = rng.gauss(68, 6)
    else:
        default_mean = rng.gauss(62, 6)

    records = []
    for course in degree_courses:
        # Only include courses up to the student's academic progress
        if course["year"] > max_year:
            continue
        if course["year"] == max_year and course["semester"] > max_semester:
            continue

        # Small chance of not having taken a course yet (5%)
        if rng.random() < 0.05:
            continue

        subject = course["subject_area"]
        mean = archetype.get(subject, default_mean) + base_offset

        mark = generate_mark(rng, mean)
        grade, grade_point = get_grade(mark)

        # Determine status
        if mark < MINIMUM_PASS_MARK:
            # 70% chance marked as failed, 20% withdrawn, 10% still completed (D grade)
            status_roll = rng.random()
            if mark < 30:
                status = "failed"
            elif status_roll < 0.15:
                status = "withdrawn"
            else:
                status = "completed"
        else:
            status = "completed"

        records.append({
            "student_id": student_id,
            "course_id": course["course_id"],
            "course_code": course["course_code"],
            "course_name": course["course_name"],
            "degree": degree,
            "year": course["year"],
            "semester": course["semester"],
            "credits": course["credits"],
            "subject_area": subject,
            "mark": mark,
            "grade": grade,
            "grade_point": grade_point,
            "status": status,
            "archetype": archetype_name,
        })

    return records


def main():
    """Generate the synthetic dataset."""
    print("=" * 60)
    print("Synthetic Student Dataset Generator")
    print(f"Seed: {SYNTHETIC_SEED}")
    print(f"Target count: {SYNTHETIC_STUDENT_COUNT} students")
    print("=" * 60)

    rng = random.Random(SYNTHETIC_SEED)
    courses = load_courses()
    print(f"Loaded {len(courses)} courses")

    all_records = []
    for student_id in range(1, SYNTHETIC_STUDENT_COUNT + 1):
        records = generate_student(rng, student_id, courses)
        all_records.extend(records)

    # Write output
    if all_records:
        fieldnames = list(all_records[0].keys())
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records)

    print(f"\nGenerated {SYNTHETIC_STUDENT_COUNT} students")
    print(f"Total course records: {len(all_records)}")
    print(f"Average courses per student: {len(all_records) / SYNTHETIC_STUDENT_COUNT:.1f}")
    print(f"Output: {OUTPUT_FILE}")

    # Stats
    archetypes = {}
    for r in all_records:
        archetypes[r["archetype"]] = archetypes.get(r["archetype"], 0) + 1
    print("\nArchetype distribution:")
    for arch, count in sorted(archetypes.items()):
        print(f"  {arch}: {count} records")

    print("\n[OK] Dataset generated successfully!")


if __name__ == "__main__":
    main()
