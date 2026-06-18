from __future__ import annotations

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    user_id: str
    title: str = Field(default="Learning Session")


class SessionRead(BaseModel):
    id: str
    user_id: str
    title: str
    status: str
    metadata_json: dict

    model_config = {"from_attributes": True}


class AttemptCreate(BaseModel):
    question_id: str
    user_id: str
    answer_text: str
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
