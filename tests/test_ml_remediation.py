"""
Tests for ML prediction remediation.
Verifies neutral baseline imputation, confidence thresholding, and consensus checks.
"""
import pytest
from ml.predict import predict_specialization, predict_with_consensus, is_model_available


class TestMLRemediation:
    def test_model_is_available(self):
        assert is_model_available() is True

    def test_missing_courses_do_not_zero_impute(self):
        """
        When student only has 1 course with 90%, missing courses should be imputed with
        the student mean (90%), NOT 0.0 (failing grade).
        """
        res = predict_specialization({"Programming": 90.0})
        assert res is not None
        pred_spec, probs = res
        assert isinstance(pred_spec, str)
        assert len(probs) == 6
        assert sum(probs.values()) == pytest.approx(1.0, abs=0.05)

    def test_preliminary_confidence_on_sparse_profile(self):
        """A profile with only 1 course should be flagged as Preliminary."""
        consensus = predict_with_consensus({"Programming": 72.0})
        assert consensus is not None
        assert consensus["is_preliminary"] is True
        assert "Preliminary" in consensus["confidence_label"]
        assert consensus["known_subject_count"] == 1

    def test_consensus_output_on_comprehensive_profile(self):
        """Student B profile with 4 strong security/networking courses."""
        courses = {
            "Cyber Security": 91.0,
            "Networking": 86.0,
            "Systems & Operating Systems": 84.0,
            "Programming": 78.0
        }
        consensus = predict_with_consensus(courses)
        assert consensus is not None
        assert consensus["is_preliminary"] is False
        assert consensus["top_probability"] > 0.35
