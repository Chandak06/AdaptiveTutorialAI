from __future__ import annotations

from learner_model.bkt import BKTState, bkt_update
from learner_model.misconceptions import detect_misconception
from learner_model.service import LearnerModelService
from storage.database import init_db, session_scope
from users.service import UserService


def test_bkt_update_improves_on_correct_answer():
    before = BKTState(mastery=0.2)
    after = bkt_update(before, True)
    assert after > 0.2


def test_misconception_detection():
    assert detect_misconception(False, 0.8)
    assert not detect_misconception(True, 0.9)


def test_learner_service_updates_state():
    init_db()
    with session_scope() as db:
        user = UserService(db).create_user("learner@example.com", "StrongPass123!", "Learner")
        service = LearnerModelService(db)
        state = service.ensure_state(user.id, "variables")
        result = {
            "correct": False,
            "confidence": 0.9,
            "recommended_difficulty": 3,
            "misconception": "scope confusion",
            "answer_text": "x is always global",
        }
        updated = service.apply_evaluation(user.id, "variables", result)
        assert updated.mastery >= 0.0
        assert "scope confusion" in updated.misconceptions
