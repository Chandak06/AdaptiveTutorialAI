from __future__ import annotations

import uuid
from sqlalchemy.orm import Session

from auth.security import hash_password
from storage import models
from storage.repositories import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def create_user(self, email: str, password: str, full_name: str | None = None, role: str = "learner") -> models.User:
        if self.users.get_by_email(email):
            raise ValueError("Email already registered")
        user = models.User(
            id=str(uuid.uuid4()),
            email=email,
            full_name=full_name,
            password_hash=hash_password(password),
            role=role,
        )
        self.users.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: str) -> models.User | None:
        return self.users.get(user_id)

    def update_profile(self, user_id: str, full_name: str | None = None, role: str | None = None) -> models.User:
        user = self.users.get(user_id)
        if user is None:
            raise ValueError("User not found")
        if full_name is not None:
            user.full_name = full_name
        if role is not None:
            user.role = role
        self.db.commit()
        self.db.refresh(user)
        return user
