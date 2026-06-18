from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None
    role: str = "learner"


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    role: str | None = None
