"""
FastAPI Serverless Application Entry Point for Vercel Deployment.
Exposes RESTful endpoints for the AI-Based IT Specialization & Course Recommendation System.

Key Architectural Guarantees:
1. 100% Stateless: computations run in-memory; no write-locks on read-only serverless filesystems.
2. Direct Reuse: leverages src/ai, src/academic, src/data, and ml modules as libraries.
3. CORS Enabled: seamless requests from Vite/React frontend and local dev environments.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure project root is on sys.path for serverless execution
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.academic.gpa import calculate_gpa, get_gpa_classification
from src.academic.grading import mark_to_grade
from src.academic.profile import build_academic_profile
from src.ai.explanations import generate_all_explanations
from src.ai.recommendation_engine import generate_recommendations
from src.ai.rule_engine import get_course_recommendations
from src.config.settings import (
    ACADEMIC_WEIGHT,
    GRADUATION_MIN_GPA_CREDITS,
    GRADUATION_MIN_NGPA_CREDITS,
    INTEREST_WEIGHT,
    SPECIALIZATION_WEIGHTS,
    Specialization,
)
from src.data import database as db
from src.data.demo_profiles import DEMO_PROFILES, get_all_demo_profiles
from ml.predict import is_model_available, load_metrics, predict_with_consensus

app = FastAPI(
    title="AI Academic Advisor API",
    description="FastAPI serverless backend for KDU IT Specialization Recommender",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend built assets for seamless SPA serving
DIST_DIR = ROOT_DIR / "frontend" / "dist"
ASSETS_DIR = DIST_DIR / "assets"
INDEX_HTML = DIST_DIR / "index.html"

if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

@app.get("/", include_in_schema=False)
@app.get("/index.html", include_in_schema=False)
def serve_index():
    if INDEX_HTML.exists():
        return FileResponse(str(INDEX_HTML))
    return HTMLResponse("<h1>KDU Academic Advisor</h1><p>API is active. Visit <a href='/docs'>/docs</a>.</p>")

@app.get("/favicon.svg", include_in_schema=False)
def serve_favicon():
    fav = ROOT_DIR / "frontend" / "public" / "favicon.svg"
    if fav.exists():
        return FileResponse(str(fav), media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="Favicon not found")


# =============================================================================
# Request / Response Schemas
# =============================================================================

class CourseRecordInput(BaseModel):
    course_id: Optional[int] = None
    course_code: str
    course_name: Optional[str] = None
    credits: Optional[int] = None
    subject_area: Optional[str] = None
    mark: float = Field(ge=0.0, le=100.0)
    course_type: Optional[str] = None
    status: Optional[str] = "completed"
    year: Optional[int] = None
    semester: Optional[int] = None


class RecommendationRequest(BaseModel):
    degree: str
    year: int = Field(ge=1, le=4, default=2)
    semester: int = Field(ge=1, le=2, default=2)
    courses: List[CourseRecordInput]
    interests: Dict[str, float] = {}  # {subject_area: intensity_1_to_5}
    academic_weight: Optional[float] = ACADEMIC_WEIGHT
    interest_weight: Optional[float] = INTEREST_WEIGHT


class AdvisorRequest(BaseModel):
    degree: str
    year: int = Field(ge=1, le=4, default=2)
    semester: int = Field(ge=1, le=2, default=2)
    courses: List[CourseRecordInput]
    target_specialization: Optional[str] = None
    degree_filter: Optional[str] = None


class GraduationAuditRequest(BaseModel):
    degree: str
    courses: List[CourseRecordInput]


# =============================================================================
# Helpers
# =============================================================================

def _hydrate_course_records(
    inputs: List[CourseRecordInput],
    catalog_by_code: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Convert input courses into complete academic course records with grade/points."""
    records = []
    for inp in inputs:
        code = inp.course_code.strip().upper()
        cat = catalog_by_code.get(code)
        grade, grade_point = mark_to_grade(inp.mark)

        if cat:
            c_id = inp.course_id or cat.get("course_id", 0)
            c_name = inp.course_name or cat.get("course_name", code)
            c_credits = inp.credits if inp.credits is not None else int(cat.get("credits", 2))
            c_area = inp.subject_area or cat.get("subject_area", "General")
            c_type = inp.course_type or cat.get("course_type", "Core")
            c_year = inp.year or cat.get("year", 1)
            c_sem = inp.semester or cat.get("semester", 1)
        else:
            c_id = inp.course_id or 999
            c_name = inp.course_name or code
            c_credits = inp.credits if inp.credits is not None else 3
            c_area = inp.subject_area or "General"
            c_type = inp.course_type or "Core"
            c_year = inp.year or 1
            c_sem = inp.semester or 1

        records.append({
            "student_id": 1,
            "course_id": c_id,
            "course_code": code,
            "course_name": c_name,
            "credits": c_credits,
            "subject_area": c_area,
            "mark": float(inp.mark),
            "grade": grade,
            "grade_point": float(grade_point),
            "status": inp.status or "completed",
            "course_type": c_type,
            "year": c_year,
            "semester": c_sem,
        })
    return records


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "ml_models_ready": is_model_available(),
    }


@app.get("/api/catalog/degrees")
def get_degrees():
    try:
        degrees = db.get_all_degrees()
        formatted = [
            {
                "degree_id": d["degree_id"],
                "name": d["name"],
                "degree_name": d["name"],
            }
            for d in degrees
        ]
        return {"degrees": formatted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/catalog/courses")
def get_courses(degree: Optional[str] = None, course_type: Optional[str] = None):
    try:
        courses = db.get_all_courses(degree=degree, course_type=course_type)
        return {"courses": courses, "total": len(courses)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/catalog/interests")
def get_interests():
    try:
        interests = db.get_all_interests()
        return {"interests": interests}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/catalog/specializations")
def get_specializations():
    try:
        specs = db.get_all_specializations()
        return {"specializations": specs, "weights": SPECIALIZATION_WEIGHTS}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/catalog/demo-profiles")
def get_demo_profiles(
    degree: Optional[str] = Query(None, description="Degree program filter"),
    year: Optional[int] = Query(None, description="Current student academic year"),
    semester: Optional[int] = Query(None, description="Current student academic semester"),
):
    """Return demo student profiles with pre-resolved course records for the requested academic stage."""
    try:
        profiles_data = get_all_demo_profiles(degree=degree, year=year, semester=semester)
        all_courses = {c["course_code"]: c for c in db.get_all_courses()}
        result = {}
        for key, demo in profiles_data.items():
            resolved_courses = []
            for item in demo["courses"]:
                if len(item) == 2:
                    code, mark = item
                    cat = all_courses.get(code, {})
                    grade, gp = mark_to_grade(mark)
                    resolved_courses.append({
                        "course_id": cat.get("course_id", 0),
                        "course_code": code,
                        "course_name": cat.get("course_name", code),
                        "credits": cat.get("credits", 3),
                        "subject_area": cat.get("subject_area", "General"),
                        "mark": mark,
                        "grade": grade,
                        "grade_point": gp,
                        "course_type": cat.get("course_type", "Core"),
                        "status": "completed",
                        "year": cat.get("year", 1),
                        "semester": cat.get("semester", 1),
                    })
                elif len(item) == 6:
                    code, mark, name, area, c_type, credits = item
                    grade, gp = mark_to_grade(mark)
                    resolved_courses.append({
                        "course_id": 999,
                        "course_code": code,
                        "course_name": name,
                        "credits": credits,
                        "subject_area": area,
                        "mark": mark,
                        "grade": grade,
                        "grade_point": gp,
                        "course_type": c_type,
                        "status": "completed",
                        "year": demo.get("year", 2),
                        "semester": demo.get("semester", 2),
                    })

            interest_dict = {area: 4.0 for area in demo.get("interests", [])}

            result[key] = {
                "key": key,
                "title": demo["title"],
                "description": demo["description"],
                "degree": demo["degree"],
                "year": demo["year"],
                "semester": demo["semester"],
                "courses": resolved_courses,
                "interests": interest_dict,
            }
        return {"profiles": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/gpa/calculate")
def calculate_student_gpa(courses: List[CourseRecordInput]):
    """Stateless GPA calculation with class rank and credit totals."""
    catalog = {c["course_code"]: c for c in db.get_all_courses()}
    records = _hydrate_course_records(courses, catalog)
    gpa, earned, attempted = calculate_gpa(records)
    classification = get_gpa_classification(gpa)
    return {
        "gpa": gpa,
        "credits_earned": earned,
        "credits_attempted": attempted,
        "classification": classification,
        "course_count": len(records),
    }


@app.post("/api/recommendations")
def get_recommendations(req: RecommendationRequest):
    """
    Execute the hybrid recommendation pipeline in-memory:
    1. Weighted Academic Fit (AI Concept 2)
    2. Content-Based Interest Matching (AI Concept 3)
    3. Hybrid combination (configurable weights)
    4. Explainable AI explanations & counterfactual pathways
    5. Machine Learning consensus cross-check (AI Concept 4)
    """
    catalog = {c["course_code"]: c for c in db.get_all_courses()}
    course_records = _hydrate_course_records(req.courses, catalog)

    profile = build_academic_profile(
        student_id=1,
        degree=req.degree,
        year=req.year,
        semester=req.semester,
        course_records=course_records,
    )

    recs = generate_recommendations(
        profile=profile,
        selected_interests=req.interests,
        academic_weight=req.academic_weight if req.academic_weight is not None else ACADEMIC_WEIGHT,
        interest_weight=req.interest_weight if req.interest_weight is not None else INTEREST_WEIGHT,
    )

    explanations = generate_all_explanations(recs)

    rec_list = []
    for r in recs:
        rec_list.append({
            "specialization_name": r.specialization_name,
            "academic_fit": r.academic_fit,
            "interest_alignment": r.interest_alignment,
            "final_score": r.final_score,
            "evidence_level": r.evidence_level,
            "relevant_course_count": r.relevant_course_count,
            "calibrated_fit": r.calibrated_fit,
            "confidence_score": r.confidence_score,
            "confidence_level": r.confidence_level,
            "rank": r.rank,
            "subject_contributions": r.subject_contributions,
            "subject_marks": r.subject_marks,
            "interest_contributions": r.interest_contributions,
            "available_subject_areas": r.available_subject_areas,
            "missing_subject_areas": r.missing_subject_areas,
        })

    exp_dict = {}
    for name, exp in explanations.items():
        exp_dict[name] = {
            "specialization_name": exp.specialization_name,
            "summary": exp.summary,
            "strengths": exp.strengths,
            "weaknesses": exp.weaknesses,
            "interest_matches": exp.interest_matches,
            "evidence_note": exp.evidence_note,
            "missing_areas_note": exp.missing_areas_note,
            "comparison_notes": exp.comparison_notes,
            "counterfactuals": exp.counterfactuals,
        }

    # ML Cross-Check
    subject_averages = {
        area: perf.average_mark
        for area, perf in profile.subject_performances.items()
    }
    ml_crosscheck = predict_with_consensus(subject_averages)

    # Sensitivity Analysis Curve
    sensitivity = []
    for w in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        pt = {"academic_weight": w, "interest_weight": round(1.0 - w, 1)}
        for r in recs:
            s = round(r.academic_fit * w + r.interest_alignment * (1.0 - w), 2)
            pt[r.specialization_name] = s
        sensitivity.append(pt)

    perf_list = [
        {
            "subject_area": p.subject_area,
            "average_mark": p.average_mark,
            "course_count": p.course_count,
            "total_credits": p.total_credits,
        }
        for p in profile.subject_performances.values()
    ]

    return {
        "profile": {
            "degree": profile.degree,
            "year": profile.year,
            "semester": profile.semester,
            "gpa": profile.gpa,
            "total_credits": profile.total_credits,
            "academic_stage": profile.academic_stage,
            "completed_course_count": profile.completed_course_count,
            "subject_performances": perf_list,
        },
        "recommendations": rec_list,
        "explanations": exp_dict,
        "ml_crosscheck": ml_crosscheck,
        "sensitivity_curve": sensitivity,
        "weights": {
            "academic_weight": req.academic_weight if req.academic_weight is not None else ACADEMIC_WEIGHT,
            "interest_weight": req.interest_weight if req.interest_weight is not None else INTEREST_WEIGHT,
        },
    }


@app.post("/api/electives/advisor")
def get_electives_and_roadmap(req: AdvisorRequest):
    """
    Rule-Based Course & Elective Advisor:
    1. Prerequisite verification
    2. Stage eligibility gating
    3. Synergy scoring against target specialization
    4. Categorization into Recommended Now / Recommended Later / Low Priority
    """
    catalog = {c["course_code"]: c for c in db.get_all_courses()}
    course_records = _hydrate_course_records(req.courses, catalog)

    profile = build_academic_profile(
        student_id=1,
        degree=req.degree,
        year=req.year,
        semester=req.semester,
        course_records=course_records,
    )

    target_spec = req.target_specialization or "Data Science"
    target_areas = set(SPECIALIZATION_WEIGHTS.get(target_spec, {}).keys())

    all_courses = db.get_all_courses(degree=req.degree_filter or req.degree)
    all_prereqs = db.get_all_prerequisites()

    recommendations = get_course_recommendations(
        profile=profile,
        all_courses=all_courses,
        all_prerequisites=all_prereqs,
        top_specialization_areas=target_areas,
        degree_filter=req.degree_filter or req.degree,
        top_specialization_name=target_spec,
    )

    serialized_recs = []
    for r in recommendations:
        serialized_recs.append({
            "course": {
                "course_id": r.course.course_id,
                "course_code": r.course.course_code,
                "course_name": r.course.course_name,
                "degree": r.course.degree,
                "year": r.course.year,
                "semester": r.course.semester,
                "credits": r.course.credits,
                "subject_area": r.course.subject_area,
                "course_type": r.course.course_type,
            },
            "category": r.category,
            "reason": r.reason,
            "missing_prerequisites": r.missing_prerequisites,
            "prerequisite_status": r.prerequisite_status,
            "chain_impact_count": r.chain_impact_count,
            "synergy_score": r.synergy_score,
            "target_specialization": r.target_specialization,
        })

    electives = [r for r in serialized_recs if r["course"]["course_type"] == "Elective"]
    cores = [r for r in serialized_recs if r["course"]["course_type"] == "Core"]
    ngpa = [r for r in serialized_recs if r["course"]["course_type"] == "NGPA"]

    roadmap = {}
    for y in range(1, 5):
        roadmap[f"Year {y}"] = {}
        for s in range(1, 3):
            sem_courses = [
                c for c in all_courses
                if c["year"] == y and c["semester"] == s
            ]
            roadmap[f"Year {y}"][f"Semester {s}"] = sem_courses

    return {
        "target_specialization": target_spec,
        "electives": electives,
        "core_courses": cores,
        "ngpa_courses": ngpa,
        "roadmap": roadmap,
        "total_available": len(serialized_recs),
    }


@app.post("/api/audit/graduation")
def audit_graduation(req: GraduationAuditRequest):
    """Graduation Credit Audit: evaluate 120 GPA and 14 NGPA credit requirements & prerequisite bottlenecks."""
    catalog = {c["course_code"]: c for c in db.get_all_courses()}
    records = _hydrate_course_records(req.courses, catalog)

    core_credits = sum(r["credits"] for r in records if r["course_type"] == "Core")
    elec_credits = sum(r["credits"] for r in records if r["course_type"] == "Elective")
    gpa_credits = core_credits + elec_credits
    ngpa_credits = sum(r["credits"] for r in records if r["course_type"] == "NGPA")
    total_earned = gpa_credits + ngpa_credits
    gpa, _, _ = calculate_gpa(records)
    classification = get_gpa_classification(gpa)

    gpa_pct = min(100.0, round((gpa_credits / GRADUATION_MIN_GPA_CREDITS) * 100, 1))
    ngpa_pct = min(100.0, round((ngpa_credits / GRADUATION_MIN_NGPA_CREDITS) * 100, 1))
    is_eligible = (gpa_credits >= GRADUATION_MIN_GPA_CREDITS) and (ngpa_credits >= GRADUATION_MIN_NGPA_CREDITS)

    # Calculate real prerequisite bottlenecks
    from collections import defaultdict
    all_deg_courses = db.get_all_courses(degree=req.degree)
    deg_course_ids = {c["course_id"] for c in all_deg_courses}
    deg_course_map = {c["course_id"]: c for c in all_deg_courses}
    completed_ids = {r["course_id"] for r in records}

    all_prereqs = db.get_all_prerequisites()
    downstream_counts = defaultdict(int)
    for p in all_prereqs:
        if p["course_id"] in deg_course_ids:
            prereq_id = p["prerequisite_course_id"]
            if prereq_id not in completed_ids and prereq_id in deg_course_map:
                downstream_counts[prereq_id] += 1

    bottlenecks = [
        f"{deg_course_map[cid]['course_code']} — {deg_course_map[cid]['course_name']} (Year {deg_course_map[cid]['year']}, Sem {deg_course_map[cid]['semester']}): Blocks {count} downstream courses."
        for cid, count in sorted(downstream_counts.items(), key=lambda x: x[1], reverse=True)
        if count >= 2
    ]

    # Check for failed core courses
    failed_courses = [r for r in records if r["mark"] < 50.0 and r["course_type"] == "Core"]
    if failed_courses:
        names = ", ".join(c["course_code"] for c in failed_courses)
        bottlenecks.insert(0, f"Core courses below passing standing (repeat required): {names}.")

    return {
        "gpa": gpa,
        "classification": classification,
        "core_credits": core_credits,
        "elective_credits": elec_credits,
        "gpa_credits_earned": gpa_credits,
        "gpa_target": GRADUATION_MIN_GPA_CREDITS,
        "gpa_progress_pct": gpa_pct,
        "ngpa_credits_earned": ngpa_credits,
        "ngpa_target": GRADUATION_MIN_NGPA_CREDITS,
        "ngpa_progress_pct": ngpa_pct,
        "total_credits_earned": total_earned,
        "is_eligible": is_eligible,
        "bottlenecks": bottlenecks[:5],
    }
