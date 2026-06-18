from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from statistics import mean
from sqlalchemy.orm import Session

from learner_model.bkt import BKTState, bkt_update
from learner_model.misconceptions import MisconceptionCatalog
from storage import models
from storage.repositories import LearnerStateRepository


class LearnerModelService:
    def __init__(self, db: Session):
        self.db = db
        self.states = LearnerStateRepository(db)
        self.catalog = MisconceptionCatalog()

    def ensure_state(self, user_id: str, concept_slug: str) -> models.LearnerState:
        state = self.states.get(user_id, concept_slug)
        if state is not None:
            return state
        state = models.LearnerState(
            id=str(uuid.uuid4()),
            user_id=user_id,
            concept_slug=concept_slug,
            mastery=0.25,
            confidence=0.25,
            retention=0.5,
            learning_velocity=0.0,
            revision_frequency=0,
            error_patterns=[],
            misconceptions=[],
            revision_due_turn=0,
            revision_due_at=datetime.utcnow(),
        )
        self.states.add(state)
        self.db.flush()
        return state

    def apply_evaluation(self, user_id: str, concept_slug: str, evaluation: dict) -> models.LearnerState:
        state = self.ensure_state(user_id, concept_slug)
        correct = bool(evaluation["correct"])
        confidence = float(evaluation.get("confidence", 0.5))
        difficulty = int(evaluation.get("recommended_difficulty", 3))
        bkt = BKTState(mastery=state.mastery)
        mastery = bkt_update(bkt, correct)
        mastery += (0.02 * difficulty) if correct else (-0.03 * max(1, difficulty))
        mastery = max(0.0, min(1.0, mastery))

        confidence_target = max(0.0, min(1.0, (confidence * 0.7) + (0.3 if correct else 0.1)))
        state.learning_velocity = round((mastery - state.mastery) * 0.8 + state.learning_velocity * 0.2, 4)
        state.mastery = round(mastery, 4)
        state.confidence = round((state.confidence * 0.6) + (confidence_target * 0.4), 4)
        state.retention = round(max(0.0, min(1.0, state.retention + (0.04 if correct else -0.05))), 4)
        state.revision_frequency += 1 if not correct or state.retention < 0.45 else 0

        if not correct:
            concept_label = concept_slug.replace("-", " ")
            suggestion = evaluation.get("misconception") or self.catalog.suggestions(concept_label)[0]
            current_misconceptions = list(state.misconceptions or [])
            if suggestion not in current_misconceptions:
                current_misconceptions.append(suggestion)
            state.misconceptions = current_misconceptions

            current_patterns = list(state.error_patterns or [])
            current_patterns.append(
                {
                    "answer": evaluation.get("answer_text", ""),
                    "misconception": suggestion,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
            state.error_patterns = current_patterns

        state.revision_due_at = datetime.utcnow() + timedelta(days=max(1, 7 - int(state.retention * 5)))
        self.db.commit()
        self.db.refresh(state)
        return state

    def summary(self, user_id: str) -> dict:
        states = self.states.list_by_user(user_id)
        if not states:
            return {"mastery": 0.0, "confidence": 0.0, "retention": 0.0, "weaknesses": []}
        mastery = mean(s.mastery for s in states)
        confidence = mean(s.confidence for s in states)
        retention = mean(s.retention for s in states)
        weaknesses = sorted(states, key=lambda s: (s.mastery, s.retention))[:5]
        return {
            "mastery": round(mastery, 4),
            "confidence": round(confidence, 4),
            "retention": round(retention, 4),
            "weaknesses": [s.concept_slug for s in weaknesses],
            "misconceptions": [m for s in states for m in s.misconceptions][:10],
        }
