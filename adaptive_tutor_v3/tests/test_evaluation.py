from __future__ import annotations

import uuid

from evaluation.engine import EvaluationEngine
from storage import models


def test_evaluation_returns_structured_payload():
    question = models.QuestionRecord(
        id=str(uuid.uuid4()),
        session_id=None,
        concept_slug="fraction-addition",
        topic="Fractions",
        blueprint_json={},
        question_type="mcq",
        prompt="2/3 + 1/2 = ?",
        options_json=["7/6", "3/5", "2/5", "1"],
        correct_answer="7/6",
        explanation="",
        difficulty=4,
        bloom_level="apply",
        metadata_json={},
    )
    learner = models.LearnerState(
        id=str(uuid.uuid4()),
        user_id=str(uuid.uuid4()),
        concept_slug="fraction-addition",
        mastery=0.3,
        confidence=0.2,
        retention=0.5,
        learning_velocity=0.0,
        revision_frequency=0,
        error_patterns=[],
        misconceptions=[],
        revision_due_turn=0,
        revision_due_at=None,
    )
    result = EvaluationEngine().evaluate(question, "7/6", learner, confidence=0.8)
    assert result["correct"] is True
    assert 0.0 <= result["confidence"] <= 1.0
    assert "mastery_change" in result
