from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import db_session
from evaluation.engine import EvaluationEngine
from storage import models

router = APIRouter()


@router.post("/attempt")
def evaluate_attempt(question_id: str, answer_text: str, confidence: float = 0.5, db: Session = Depends(db_session)):
    question = db.get(models.QuestionRecord, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    result = EvaluationEngine().evaluate(question, answer_text, confidence=confidence)
    return result
