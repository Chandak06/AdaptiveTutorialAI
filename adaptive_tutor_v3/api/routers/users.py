from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import current_user, db_session
from learner_model.service import LearnerModelService
from users.schemas import UserProfileUpdate, UserRead
from users.service import UserService

router = APIRouter()


@router.get("/me", response_model=UserRead)
def me(user=Depends(current_user)):
    return user


@router.patch("/me", response_model=UserRead)
def update_me(payload: UserProfileUpdate, user=Depends(current_user), db: Session = Depends(db_session)):
    try:
        updated = UserService(db).update_profile(user.id, full_name=payload.full_name, role=payload.role)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return updated


@router.get("/{user_id}/learner-state")
def learner_state(user_id: str, db: Session = Depends(db_session)):
    service = LearnerModelService(db)
    states = service.summary(user_id)
    return states
