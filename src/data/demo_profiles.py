"""
Demonstration & Testing Student Profiles.
Provides realistic archetypes for live presentations, video recording, and testing.
Supports dynamic stage-aware course generation based on user's current Year and Semester.
"""
from typing import Dict, List, Any, Optional
from src.data import database as db
from src.academic.grading import mark_to_grade

ARCHETYPE_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "student_a": {
        "title": "Student A — Data Science Focus",
        "description": "Strong in Statistics, Data Analysis, Database, and Mathematics; aims for Data Science.",
        "default_degree": "Information Technology",
        "default_year": 2,
        "default_semester": 2,
        "interests": ["Data Analysis", "Statistics", "Database", "Mathematics"],
        "base_marks": {
            "Statistics": 92.0,
            "Data Analysis": 90.0,
            "Database": 88.0,
            "Mathematics": 88.0,
            "Artificial Intelligence": 88.0,
            "Programming": 85.0,
            "Algorithms & Data Structures": 82.0,
            "Systems & Operating Systems": 74.0,
            "Networking": 72.0,
            "Cyber Security": 70.0,
            "Software Engineering": 75.0,
            "Other": 75.0,
            "Cloud Computing": 76.0,
        },
        "overrides": {
            "IT1102": 85.0,
            "IT1208": 92.0,
            "IT2104": 90.0,
            "IT2103": 88.0,
            "IT1104": 88.0,
        },
    },
    "student_b": {
        "title": "Student B — Cyber Security Focus",
        "description": "Strong in Cyber Security, Networking, Systems, and Cloud; aims for Cyber Security.",
        "default_degree": "Information Technology",
        "default_year": 2,
        "default_semester": 2,
        "interests": ["Cyber Security", "Networking", "Systems & Operating Systems"],
        "base_marks": {
            "Cyber Security": 94.0,
            "Networking": 90.0,
            "Systems & Operating Systems": 88.0,
            "Cloud Computing": 86.0,
            "Programming": 80.0,
            "Algorithms & Data Structures": 78.0,
            "Database": 78.0,
            "Software Engineering": 75.0,
            "Mathematics": 74.0,
            "Other": 75.0,
            "Artificial Intelligence": 72.0,
            "Statistics": 70.0,
            "Data Analysis": 68.0,
        },
        "overrides": {
            "IT1204": 88.0,
            "IT1206": 88.0,
            "IT2105": 90.0,
            "IT3106": 94.0,
            "IT1203": 86.0,
        },
    },
    "student_c": {
        "title": "Student C — Software Engineering Focus",
        "description": "Strong in Software Engineering, Programming, DSA, and Database; SE specialist.",
        "default_degree": "Software Engineering",
        "default_year": 2,
        "default_semester": 2,
        "interests": ["Programming", "Software Engineering", "Algorithms & Data Structures"],
        "base_marks": {
            "Software Engineering": 92.0,
            "Programming": 94.0,
            "Algorithms & Data Structures": 90.0,
            "Database": 86.0,
            "Cloud Computing": 84.0,
            "Systems & Operating Systems": 82.0,
            "Networking": 80.0,
            "Artificial Intelligence": 78.0,
            "Mathematics": 76.0,
            "Other": 76.0,
            "Data Analysis": 74.0,
            "Statistics": 72.0,
            "Cyber Security": 72.0,
        },
        "overrides": {
            "SE1101": 94.0,
            "SE1202": 92.0,
            "SE2101": 90.0,
            "SE2105": 92.0,
            "SE2103": 92.0,
        },
    },
    "student_d": {
        "title": "Student D — Multidisciplinary / Conflicting Profile",
        "description": "Strong in Programming, AI, and Statistics; moderate in Security; broad interests.",
        "default_degree": "Information Technology",
        "default_year": 2,
        "default_semester": 2,
        "interests": ["Artificial Intelligence", "Data Analysis", "Cyber Security"],
        "base_marks": {
            "Programming": 90.0,
            "Artificial Intelligence": 89.0,
            "Statistics": 88.0,
            "Data Analysis": 86.0,
            "Database": 85.0,
            "Software Engineering": 84.0,
            "Mathematics": 82.0,
            "Systems & Operating Systems": 78.0,
            "Other": 76.0,
            "Networking": 72.0,
            "Cyber Security": 70.0,
            "Cloud Computing": 74.0,
        },
        "overrides": {
            "IT1102": 90.0,
            "IT1208": 88.0,
            "IT2104": 86.0,
            "IT3106": 70.0,
        },
    },
    "student_e": {
        "title": "Student E — Early-Stage Student",
        "description": "Only 1 completed course (Programming: 72); specifically tests Limited Evidence handling.",
        "default_degree": "Information Technology",
        "default_year": 1,
        "default_semester": 1,
        "interests": [],
        "static_courses": [
            ("IT1102", 72.0),
        ],
    },
    "student_f": {
        "title": "Student F — Universal / Non-KDU Student (SLIIT / IIT / Moratuwa)",
        "description": "Student from another computing faculty with custom modules mapped to standard subject areas.",
        "default_degree": "Custom / Other University Degree",
        "default_year": 2,
        "default_semester": 2,
        "interests": ["Artificial Intelligence", "Statistics"],
        "static_courses": [
            ("CS2010", 88.0, "Object Oriented Programming", "Programming", "Core", 3),
            ("IT2040", 85.0, "Database Systems & Design", "Database", "Core", 3),
            ("MA2020", 78.0, "Probability & Statistics", "Statistics", "Core", 3),
            ("EL2050", 90.0, "Machine Learning Fundamentals", "Artificial Intelligence", "Elective", 3),
            ("NG2010", 80.0, "Professional Communication", "Other", "NGPA", 2),
        ],
    },
}


def build_demo_profile(
    profile_key: str,
    degree: Optional[str] = None,
    year: Optional[int] = None,
    semester: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generate a demo profile. Autofills all completed courses strictly prior to the current (year, semester).
    If a student is in Year Y, Semester S, they have completed all courses from semesters where
    (year < Y) or (year == Y and semester < S).
    """
    if profile_key not in ARCHETYPE_TEMPLATES:
        raise ValueError(f"Unknown archetype: {profile_key}")

    tmpl = ARCHETYPE_TEMPLATES[profile_key]

    # Student E is fixed as Year 1 Semester 1 with 1 course to test Limited Evidence
    if profile_key == "student_e":
        return {
            "title": tmpl["title"],
            "description": tmpl["description"],
            "degree": tmpl["default_degree"],
            "year": 1,
            "semester": 1,
            "courses": list(tmpl["static_courses"]),
            "interests": list(tmpl["interests"]),
        }

    # Student F has custom external modules
    if profile_key == "student_f":
        return {
            "title": tmpl["title"],
            "description": tmpl["description"],
            "degree": tmpl["default_degree"],
            "year": year if year is not None else tmpl["default_year"],
            "semester": semester if semester is not None else tmpl["default_semester"],
            "courses": list(tmpl["static_courses"]),
            "interests": list(tmpl["interests"]),
        }

    actual_degree = degree or tmpl["default_degree"]
    if actual_degree == "Custom / Other University Degree":
        actual_degree = tmpl["default_degree"]

    actual_year = year if year is not None else tmpl["default_year"]
    actual_semester = semester if semester is not None else tmpl["default_semester"]

    all_courses = db.get_all_courses(degree=actual_degree)
    prior_courses = [
        c for c in all_courses
        if (c["year"] < actual_year) or (c["year"] == actual_year and c["semester"] < actual_semester)
    ]
    prior_courses.sort(key=lambda c: (c["year"], c["semester"], c["course_code"]))

    base_marks = tmpl.get("base_marks", {})
    overrides = tmpl.get("overrides", {})

    resolved_courses = []
    for c in prior_courses:
        code = c["course_code"]
        if code in overrides:
            mark = overrides[code]
        else:
            mark = base_marks.get(c["subject_area"], 75.0)
        resolved_courses.append((code, mark))

    return {
        "title": tmpl["title"],
        "description": tmpl["description"],
        "degree": actual_degree,
        "year": actual_year,
        "semester": actual_semester,
        "courses": resolved_courses,
        "interests": list(tmpl["interests"]),
    }


def get_all_demo_profiles(
    degree: Optional[str] = None,
    year: Optional[int] = None,
    semester: Optional[int] = None,
) -> Dict[str, Dict[str, Any]]:
    """Build all benchmark archetypes for the specified stage."""
    result = {}
    for key in ARCHETYPE_TEMPLATES:
        result[key] = build_demo_profile(key, degree=degree, year=year, semester=semester)
    return result


# Pre-populated dictionary for backward compatibility
DEMO_PROFILES: Dict[str, Dict[str, Any]] = get_all_demo_profiles(year=2, semester=2)


def load_demo_profile(
    profile_key: str,
    degree: Optional[str] = None,
    year: Optional[int] = None,
    semester: Optional[int] = None,
) -> bool:
    """Populate active database with the selected archetype."""
    if profile_key not in ARCHETYPE_TEMPLATES:
        return False
    data = build_demo_profile(profile_key, degree=degree, year=year, semester=semester)
    db.clear_student_data()
    sid = db.save_student(data["degree"], data["year"], data["semester"])

    all_courses = {c["course_code"]: c for c in db.get_all_courses(degree=data["degree"])}
    for entry in data["courses"]:
        if len(entry) == 2:
            code, mark = entry
            if code in all_courses:
                course = all_courses[code]
                grade, gp = mark_to_grade(mark)
                db.save_student_course(sid, course["course_id"], mark, grade, gp, "completed")
        elif len(entry) == 6:
            code, mark, name, area, course_type, credits = entry
            cid = db.save_custom_course(
                degree=data["degree"],
                course_code=code,
                course_name=name,
                year=data["year"],
                semester=data["semester"],
                credits=credits,
                subject_area=area,
                course_type=course_type,
            )
            grade, gp = mark_to_grade(mark)
            db.save_student_course(sid, cid, mark, grade, gp, "completed")

    if data["interests"]:
        all_interests = {i["name"]: i["interest_id"] for i in db.get_all_interests()}
        int_ids = [all_interests[name] for name in data["interests"] if name in all_interests]
        db.save_student_interests(sid, int_ids)
    return True
