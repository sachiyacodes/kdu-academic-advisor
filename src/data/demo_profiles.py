"""
Demonstration & Testing Student Profiles.
Provides realistic archetypes for live presentations, video recording, and testing.
"""
from typing import Dict, List, Any
from src.data import database as db
from src.academic.grading import mark_to_grade

DEMO_PROFILES: Dict[str, Dict[str, Any]] = {
    "student_a": {
        "title": "Student A — Data Science Focus",
        "description": "Strong in Statistics (88) and Programming (84); interests in Data Analysis and Statistics.",
        "degree": "Information Technology",
        "year": 2,
        "semester": 2,
        "courses": [
            ("IT1102", 84.0),
            ("IT1208", 88.0),
            ("IT1203", 80.0),
            ("IT2104", 82.0),
        ],
        "interests": ["Data Analysis", "Statistics"],
    },
    "student_b": {
        "title": "Student B — Cyber Security Focus",
        "description": "Strong in Cyber Security (91), Networking (86), and Systems (84); interests in Cyber Security and Networking.",
        "degree": "Information Technology",
        "year": 2,
        "semester": 2,
        "courses": [
            ("IT1204", 84.0),
            ("IT1206", 86.0),
            ("IT2105", 88.0),
            ("IT3106", 91.0),
        ],
        "interests": ["Cyber Security", "Networking"],
    },
    "student_c": {
        "title": "Student C — Software Engineering Focus",
        "description": "Strong in Programming (92), Software Engineering (88), and Algorithms (84); interest in Programming.",
        "degree": "Software Engineering",
        "year": 2,
        "semester": 2,
        "courses": [
            ("SE1101", 92.0),
            ("SE2101", 84.0),
            ("SE2103", 90.0),
            ("SE2105", 88.0),
        ],
        "interests": ["Programming", "Software Engineering"],
    },
    "student_d": {
        "title": "Student D — Multidisciplinary / Conflicting Profile",
        "description": "Strong in Programming (90) and Statistics (85), moderate in Security (70); broad interests.",
        "degree": "Information Technology",
        "year": 2,
        "semester": 2,
        "courses": [
            ("IT1102", 90.0),
            ("IT1208", 85.0),
            ("IT3106", 70.0),
        ],
        "interests": ["Artificial Intelligence", "Data Analysis", "Cyber Security"],
    },
    "student_e": {
        "title": "Student E — Early-Stage Student",
        "description": "Only 1 completed course (Programming: 72); tests Limited Evidence handling.",
        "degree": "Information Technology",
        "year": 1,
        "semester": 1,
        "courses": [
            ("IT1102", 72.0),
        ],
        "interests": [],
    },
}


def load_demo_profile(profile_key: str) -> bool:
    """Populate active database with the selected archetype."""
    if profile_key not in DEMO_PROFILES:
        return False
    data = DEMO_PROFILES[profile_key]
    db.clear_student_data()
    sid = db.save_student(data["degree"], data["year"], data["semester"])

    all_courses = {c["course_code"]: c for c in db.get_all_courses(degree=data["degree"])}
    for code, mark in data["courses"]:
        if code in all_courses:
            course = all_courses[code]
            grade, gp = mark_to_grade(mark)
            db.save_student_course(sid, course["course_id"], mark, grade, gp, "completed")

    if data["interests"]:
        all_interests = {i["name"]: i["interest_id"] for i in db.get_all_interests()}
        int_ids = [all_interests[name] for name in data["interests"] if name in all_interests]
        db.save_student_interests(sid, int_ids)
    return True
