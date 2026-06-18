from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import db_session
from sessions.schemas import AttemptCreate, SessionCreate
from sessions.service import SessionService

router = APIRouter()


@router.post("")
def create_session(payload: SessionCreate, db: Session = Depends(db_session)):
    return SessionService(db).create_session(payload.user_id, payload.title)


@router.post("/{session_id}/close")
def close_session(session_id: str, db: Session = Depends(db_session)):
    try:
        return SessionService(db).close_session(session_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{session_id}/attempt")
def record_attempt(session_id: str, payload: AttemptCreate, db: Session = Depends(db_session)):
    try:
        attempt, evaluation = SessionService(db).record_attempt(
            question_id=payload.question_id,
            user_id=payload.user_id,
            answer_text=payload.answer_text,
            confidence=payload.confidence,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"attempt": attempt, "evaluation": evaluation, "session_id": session_id}
