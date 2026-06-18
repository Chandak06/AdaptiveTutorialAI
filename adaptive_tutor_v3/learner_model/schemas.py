from __future__ import annotations

from pydantic import BaseModel, Field


class LearnerStateRead(BaseModel):
    user_id: str
    concept_slug: str
    mastery: float
    confidence: float
    retention: float
    learning_velocity: float
    revision_frequency: int
    error_patterns: list
    misconceptions: list

    model_config = {"from_attributes": True}


class LearnerStateUpdate(BaseModel):
    mastery: float | None = Field(default=None, ge=0.0, le=1.0)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    retention: float | None = Field(default=None, ge=0.0, le=1.0)
