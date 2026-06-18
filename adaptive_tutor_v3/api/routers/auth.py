from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import db_session
from auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from auth.service import AuthService
from users.schemas import UserRead

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(payload: RegisterRequest, db: Session = Depends(db_session)):
    try:
        user = AuthService(db).register(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(db_session)):
    try:
        token = AuthService(db).login(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return TokenResponse(access_token=token)
