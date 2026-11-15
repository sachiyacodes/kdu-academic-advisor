"""Regression checks for earned-credit and request-boundary validation."""

import pytest
from fastapi.testclient import TestClient

from api.index import app
from src.data import database as db


client = TestClient(app)


@pytest.fixture
def catalog(monkeypatch):
    courses = [
        dict(course_id=i, course_code=f"CORE{i}", course_name=f"Core {i}",
             credits=30, subject_area="Programming", course_type="Core", year=1, semester=1)
        for i in range(1, 5)
    ] + [dict(course_id=5, course_code="NGPA1", course_name="Non-GPA", credits=14,
              subject_area="Other", course_type="NGPA", year=1, semester=1)]
    monkeypatch.setattr(db, "get_all_courses", lambda **kwargs: courses)
    monkeypatch.setattr(db, "get_all_prerequisites", lambda: [])
    return courses


def test_failed_and_withdrawn_records_do_not_award_credits(catalog):
    courses = [dict(course_code=c["course_code"], mark=0) for c in catalog]
    courses[1].update(mark=90, status="withdrawn")
    result = client.post("/api/audit/graduation", json={"degree": "Test", "courses": courses})
    assert result.status_code == 200
    assert result.json()["total_credits_earned"] == 0
    assert result.json()["is_eligible"] is False
    gpa = client.post("/api/gpa/calculate", json=courses).json()
    assert gpa["credits_earned"] == 0
    assert gpa["credits_attempted"] == 90


def test_catalog_metadata_cannot_be_overridden(catalog):
    response = client.post("/api/gpa/calculate", json=[
        dict(course_code="CORE1", mark=80, credits=1, course_type="NGPA", course_id=5),
    ])
    assert response.status_code == 200
    assert response.json()["credits_earned"] == 30
    assert response.json()["credits_attempted"] == 30


def test_passing_threshold_uses_configured_rounding(catalog):
    response = client.post("/api/audit/graduation", json={
        "degree": "Test", "courses": [dict(course_code=c["course_code"], mark=39.5) for c in catalog],
    })
    assert response.status_code == 200
    assert response.json()["is_eligible"] is True
    assert response.json()["total_credits_earned"] == 134
    assert not any("repeat required" in warning for warning in response.json()["bottlenecks"])


def test_failed_core_blocks_eligibility_even_with_enough_other_credits(catalog):
    courses = [dict(course_code=c["course_code"], mark=70) for c in catalog]
    courses.append(dict(course_code="EXTRA", credits=3, course_type="Core", mark=0))
    response = client.post("/api/audit/graduation", json={"degree": "Test", "courses": courses})
    assert response.json()["total_credits_earned"] == 134
    assert response.json()["is_eligible"] is False


def test_failed_course_does_not_satisfy_prerequisites(catalog, monkeypatch):
    monkeypatch.setattr(db, "get_all_prerequisites", lambda: [
        dict(course_id=2, prerequisite_course_id=1), dict(course_id=3, prerequisite_course_id=1),
    ])
    response = client.post("/api/audit/graduation", json={
        "degree": "Test", "courses": [dict(course_code="CORE1", mark=0)],
    })
    assert any("Blocks 2 downstream" in warning for warning in response.json()["bottlenecks"])


@pytest.mark.parametrize("payload", [
    [dict(course_code="CORE1", mark=70), dict(course_code=" core1 ", mark=90)],
    [dict(course_code="CORE1", mark=70, credits=-3)],
    [dict(course_code="CORE1", mark=70, credits=1000)],
    [dict(course_code="CORE1", mark=70, status="passed")],
    [dict(course_code=" ", mark=70)],
])
def test_invalid_course_requests_are_rejected(payload, catalog):
    assert client.post("/api/gpa/calculate", json=payload).status_code == 422


@pytest.mark.parametrize("weights", [
    dict(academic_weight=100, interest_weight=100),
    dict(academic_weight=-0.1, interest_weight=1.1),
    dict(academic_weight=0.8, interest_weight=0.8),
])
def test_invalid_weights_are_rejected(weights):
    response = client.post("/api/recommendations", json={"degree": "Test", "courses": [], **weights})
    assert response.status_code == 422


@pytest.mark.parametrize("intensity", [-0.5, 5.5, "NaN", "Infinity", "-Infinity"])
def test_invalid_interest_intensities_are_rejected(intensity):
    response = client.post("/api/recommendations", json={
        "degree": "Test", "courses": [], "interests": {"Programming": intensity},
    })
    assert response.status_code == 422


@pytest.mark.parametrize("intensity", [0, 0.5, 5])
def test_interest_slider_boundaries_are_supported(intensity):
    response = client.post("/api/recommendations", json={
        "degree": "Test", "courses": [], "interests": {"Programming": intensity},
    })
    assert response.status_code == 200
    for recommendation in response.json()["recommendations"]:
        assert 0 <= recommendation["final_score"] <= 100


def test_unknown_course_cannot_impersonate_a_catalog_prerequisite(catalog):
    from api.index import CourseRecordInput, _hydrate_course_records

    records = _hydrate_course_records([CourseRecordInput(course_code="CUSTOM", course_id=1, mark=80)],
                                      {c["course_code"]: c for c in catalog})
    assert records[0]["course_id"] not in {c["course_id"] for c in catalog}
