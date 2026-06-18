from __future__ import annotations

from collections.abc import Generator
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from auth.security import decode_token
from storage.database import get_session
from storage.repositories import UserRepository


def db_session() -> Generator:
    yield from get_session()


def current_user_id(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = decode_token(token)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return payload.sub


def current_user(db: Session = Depends(db_session), authorization: str | None = Header(default=None)):
    user_id = current_user_id(authorization)
    user = UserRepository(db).get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
