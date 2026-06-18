from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from analytics.service import AnalyticsService
from api.dependencies import db_session
from storage import models

router = APIRouter()


@router.get("/student/{user_id}")
def student(user_id: str, db: Session = Depends(db_session)):
    learner_states = db.query(models.LearnerState).filter(models.LearnerState.user_id == user_id).all()
    states = [
        {
            "concept_slug": s.concept_slug,
            "mastery": s.mastery,
            "confidence": s.confidence,
            "retention": s.retention,
            "learning_velocity": s.learning_velocity,
            "misconceptions": s.misconceptions,
            "updated_at": s.updated_at.isoformat() if s.updated_at else "",
        }
        for s in learner_states
    ]
    attempts = []
    return AnalyticsService().student_analytics(states, attempts)


@router.get("/teacher")
def teacher(db: Session = Depends(db_session)):
    states = [
        {
            "concept_slug": s.concept_slug,
            "mastery": s.mastery,
            "confidence": s.confidence,
            "retention": s.retention,
            "learning_velocity": s.learning_velocity,
            "misconceptions": s.misconceptions,
        }
        for s in db.query(models.LearnerState).all()
    ]
    concepts = [
        {
            "slug": c.slug,
            "name": c.name,
            "topic": c.topic,
        }
        for c in db.query(models.Concept).all()
    ]
    return AnalyticsService().teacher_analytics(states, concepts)
