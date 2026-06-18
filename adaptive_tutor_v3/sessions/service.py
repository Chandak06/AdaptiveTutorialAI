from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from evaluation.engine import EvaluationEngine
from learner_model.service import LearnerModelService
from storage import models
from storage.repositories import AttemptRepository, QuestionRepository, SessionRepository


class SessionService:
    def __init__(self, db: Session):
        self.db = db
        self.sessions = SessionRepository(db)
        self.questions = QuestionRepository(db)
        self.attempts = AttemptRepository(db)
        self.evaluator = EvaluationEngine()
        self.learner_service = LearnerModelService(db)

    def create_session(self, user_id: str, title: str) -> models.LearningSession:
        session = models.LearningSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            status="active",
            metadata_json={"created_via": "api"},
        )
        self.sessions.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def close_session(self, session_id: str) -> models.LearningSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise ValueError("Session not found")
        session.status = "closed"
        session.ended_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(session)
        return session

    def record_attempt(self, question_id: str, user_id: str, answer_text: str, confidence: float = 0.5):
        question = self.questions.get(question_id)
        if question is None:
            raise ValueError("Question not found")
        learner_state = self.learner_service.ensure_state(user_id, question.concept_slug)
        evaluation = self.evaluator.evaluate(question, answer_text, learner_state=learner_state, confidence=confidence)
        attempt = models.AttemptRecord(
            id=str(uuid.uuid4()),
            question_id=question.id,
            session_id=question.session_id,
            user_id=user_id,
            answer_text=answer_text,
            is_correct=evaluation["correct"],
            confidence=evaluation["confidence"],
            mastery_change=evaluation["mastery_change"],
            retention_change=evaluation["retention_change"],
            misconception=evaluation["misconception"] or "",
            metadata_json={"next_action": evaluation["next_action"], "recommended_difficulty": evaluation["recommended_difficulty"]},
        )
        self.attempts.add(attempt)
        self.learner_service.apply_evaluation(user_id=user_id, concept_slug=question.concept_slug, evaluation=evaluation)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt, evaluation
