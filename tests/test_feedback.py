"""
Tests for recommendation feedback persistence.
"""
import pytest
from src.data import database as db


class TestFeedbackPersistence:
    def test_save_and_retrieve_feedback(self):
        """Verify recommendation feedback is successfully inserted and fetched."""
        fb_id = db.save_student_feedback(
            student_id=None,
            specialization_name="Data Science",
            rating=1,
            comment="Very accurate recommendation!"
        )
        assert fb_id is not None
        assert fb_id > 0

        feedback_list = db.get_student_feedback()
        assert len(feedback_list) > 0
        recent = feedback_list[0]
        assert recent["specialization_name"] == "Data Science"
        assert recent["rating"] == 1
