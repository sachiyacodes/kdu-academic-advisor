# Database Schema

## Architecture (FIX-1)

CSV files under `data/` are the **single source of truth** for all static/configuration data. SQLite (`database/academic.db`) is populated from those CSVs via `scripts/seed_database.py` and is the only thing the running application queries against.

```
CSV files (data/) --seed_database.py--> SQLite (database/academic.db)
                                              |
                                     Streamlit app reads/writes
                                     ONLY through SQLite at runtime
```

## Tables

### subject_areas
Canonical 13-item taxonomy (Section 9).

| Column | Type | Constraints |
|--------|------|-------------|
| subject_area_id | INTEGER | PRIMARY KEY |
| name | TEXT | NOT NULL, UNIQUE |

### degrees
Supported degree programs.

| Column | Type | Constraints |
|--------|------|-------------|
| degree_id | INTEGER | PRIMARY KEY |
| name | TEXT | NOT NULL, UNIQUE |

### courses
Curriculum courses (444 courses across 6 KDU computing degrees + Universal Custom Mode).

| Column | Type | Constraints |
|--------|------|-------------|
| course_id | INTEGER | PRIMARY KEY |
| course_code | TEXT | NOT NULL, UNIQUE |
| course_name | TEXT | NOT NULL |
| degree | TEXT | NOT NULL, FK -> degrees.name |
| year | INTEGER | CHECK(1-4) |
| semester | INTEGER | CHECK(1-2) |
| credits | INTEGER | CHECK(credits >= 0) |
| subject_area | TEXT | NOT NULL, FK -> subject_areas.name |
| course_type | TEXT | NOT NULL DEFAULT 'Core' CHECK(course_type IN ('Core', 'Elective', 'NGPA')) |

### specializations
Specialization categories (6 prototype specializations).

| Column | Type | Constraints |
|--------|------|-------------|
| specialization_id | INTEGER | PRIMARY KEY |
| name | TEXT | NOT NULL, UNIQUE |
| description | TEXT | |

### specialization_weights
Academic weights for scoring (Section 11).

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| specialization_id | INTEGER | FK -> specializations |
| specialization_name | TEXT | NOT NULL |
| subject_area | TEXT | FK -> subject_areas.name |
| weight | REAL | CHECK(0-1) |

**Constraint:** Each specialization's weights must sum to 1.0.

### specialization_interests
Interest weight vectors for interest matching (FIX-3).

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| specialization_id | INTEGER | FK -> specializations |
| specialization_name | TEXT | NOT NULL |
| subject_area | TEXT | FK -> subject_areas.name |
| weight | REAL | CHECK(0-1) |

**Design:** Uses the same canonical subject-area taxonomy as academic weights — not a separate interest table.

### prerequisites
Course prerequisite relationships (290 prerequisite dependencies).

| Column | Type | Constraints |
|--------|------|-------------|
| prerequisite_id | INTEGER | PRIMARY KEY |
| course_id | INTEGER | FK -> courses |
| prerequisite_course_id | INTEGER | FK -> courses |

### interests
Available interest options (mapped 1:1 to subject areas per Section 21).

| Column | Type | Constraints |
|--------|------|-------------|
| interest_id | INTEGER | PRIMARY KEY |
| name | TEXT | NOT NULL, UNIQUE |
| subject_area | TEXT | FK -> subject_areas.name |

### students (runtime)
Student profile data.

| Column | Type | Constraints |
|--------|------|-------------|
| student_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| degree | TEXT | NOT NULL, FK -> degrees.name |
| year | INTEGER | CHECK(1-4) |
| semester | INTEGER | CHECK(1-2) |

### student_courses (runtime)
Student course records with marks.

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| student_id | INTEGER | FK -> students |
| course_id | INTEGER | FK -> courses |
| mark | REAL | CHECK(0-100) |
| grade | TEXT | NOT NULL |
| grade_point | REAL | CHECK(0-4) |
| status | TEXT | CHECK IN (completed, failed, withdrawn, in_progress) |
| | | UNIQUE(student_id, course_id) |

### student_interests (runtime)
Student interest selections with continuous intensity weighting.

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| student_id | INTEGER | FK -> students |
| interest_id | INTEGER | FK -> interests |
| intensity | REAL | DEFAULT 3.0 |
| | | UNIQUE(student_id, interest_id) |

### student_feedback (runtime)
Human-in-the-loop recommendation feedback.

| Column | Type | Constraints |
|--------|------|-------------|
| feedback_id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| student_id | INTEGER | FK -> students |
| specialization_name | TEXT | NOT NULL |
| rating | INTEGER | NOT NULL (-1 or 1) |
| comment | TEXT | |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

## Security & Integrity
- All queries use parameterized statements (no SQL injection)
- Foreign keys enforced via `PRAGMA foreign_keys = ON`
- CHECK constraints validate data ranges and taxonomy adherence
- Zero data leakage on reset: `clear_student_data` cleans runtime tables and custom courses
