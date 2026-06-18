from __future__ import annotations

import uuid
from sqlalchemy.orm import Session

from auth.security import create_token, hash_password, verify_password
from auth.schemas import RegisterRequest
from storage import models
from storage.repositories import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def register(self, payload: RegisterRequest) -> models.User:
        if self.users.get_by_email(payload.email):
            raise ValueError("Email already registered")
        user = models.User(
            id=str(uuid.uuid4()),
            email=str(payload.email),
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
            role=payload.role,
        )
        self.users.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, email: str, password: str) -> str:
        user = self.users.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return create_token(user.id, role=user.role)
