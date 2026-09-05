"""
Integration tests for FastAPI serverless backend (api/index.py).
Verifies all REST API endpoints using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient

from api.index import app

client = TestClient(app)


class TestAPIEndpoints:
    def test_health_check(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["ml_models_ready"] is True

    def test_catalog_degrees(self):
        response = client.get("/api/catalog/degrees")
        assert response.status_code == 200
        data = response.json()
        assert "degrees" in data
        assert len(data["degrees"]) >= 6

    def test_catalog_courses(self):
        response = client.get("/api/catalog/courses")
        assert response.status_code == 200
        data = response.json()
        assert "courses" in data
        assert data["total"] == 444

    def test_catalog_courses_filter_degree(self):
        response = client.get("/api/catalog/courses?degree=Information Technology")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0
        for c in data["courses"]:
            assert c["degree"] == "Information Technology"

    def test_catalog_interests(self):
        response = client.get("/api/catalog/interests")
        assert response.status_code == 200
        data = response.json()
        assert "interests" in data
        assert len(data["interests"]) == 13

    def test_catalog_demo_profiles(self):
        response = client.get("/api/catalog/demo-profiles")
        assert response.status_code == 200
        data = response.json()
        assert "profiles" in data
        assert "student_a" in data["profiles"]
        st_a = data["profiles"]["student_a"]
        assert st_a["degree"] == "Information Technology"
        assert len(st_a["courses"]) >= 4

    def test_gpa_calculate(self):
        payload = [
            {"course_code": "IT1102", "course_name": "Programming", "credits": 3, "mark": 85.0},
            {"course_code": "IT1208", "course_name": "Statistics", "credits": 3, "mark": 80.0},
        ]
        response = client.post("/api/gpa/calculate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["gpa"] == 3.85
        assert data["credits_earned"] == 6
        assert data["classification"] == "First Class Honours"

    def test_recommendations_pipeline(self):
        demo_resp = client.get("/api/catalog/demo-profiles")
        st_a = demo_resp.json()["profiles"]["student_a"]

        payload = {
            "degree": st_a["degree"],
            "year": st_a["year"],
            "semester": st_a["semester"],
            "courses": st_a["courses"],
            "interests": st_a["interests"],
            "academic_weight": 0.70,
            "interest_weight": 0.30,
        }
        response = client.post("/api/recommendations", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert "profile" in data
        assert data["profile"]["gpa"] == 3.64
        assert len(data["recommendations"]) == 6

        # Top recommendation for student A is Data Science
        top_rec = data["recommendations"][0]
        assert top_rec["specialization_name"] == "Data Science"
        assert top_rec["final_score"] > 80.0

        # Explanations present
        assert "Data Science" in data["explanations"]
        assert len(data["explanations"]["Data Science"]["strengths"]) > 0

        # ML consensus cross-check present
        assert "ml_crosscheck" in data
        assert data["ml_crosscheck"] is not None
        assert "prediction" in data["ml_crosscheck"]

        # Sensitivity curve present
        assert len(data["sensitivity_curve"]) == 9

    def test_electives_advisor(self):
        demo_resp = client.get("/api/catalog/demo-profiles")
        st_a = demo_resp.json()["profiles"]["student_a"]

        payload = {
            "degree": st_a["degree"],
            "year": st_a["year"],
            "semester": st_a["semester"],
            "courses": st_a["courses"],
            "target_specialization": "Data Science",
        }
        response = client.post("/api/electives/advisor", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["target_specialization"] == "Data Science"
        assert len(data["electives"]) > 0
        assert "roadmap" in data

    def test_graduation_audit(self):
        payload = {
            "degree": "Information Technology",
            "courses": [
                {"course_code": "IT1101", "credits": 3, "mark": 75.0, "course_type": "Core"},
                {"course_code": "IT1102", "credits": 3, "mark": 82.0, "course_type": "Core"},
                {"course_code": "NG1101", "credits": 2, "mark": 70.0, "course_type": "NGPA"},
            ],
        }
        response = client.post("/api/audit/graduation", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["gpa_credits_earned"] == 6
        assert data["ngpa_credits_earned"] == 2
        assert data["is_eligible"] is False
        assert len(data["bottlenecks"]) >= 2
