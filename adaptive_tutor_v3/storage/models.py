from __future__ import annotations

from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="learner", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    sessions: Mapped[list["LearningSession"]] = relationship(back_populates="user", cascade="all,delete-orphan")
    learner_states: Mapped[list["LearnerState"]] = relationship(back_populates="user", cascade="all,delete-orphan")


class LearningSession(Base, TimestampMixin):
    __tablename__ = "learning_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    user: Mapped["User"] = relationship(back_populates="sessions")
    attempts: Mapped[list["AttemptRecord"]] = relationship(back_populates="session", cascade="all,delete-orphan")


class Concept(Base, TimestampMixin):
    __tablename__ = "concepts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    topic: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    parent_slug: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    prerequisites: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    objectives: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)


class LearnerState(Base, TimestampMixin):
    __tablename__ = "learner_states"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True, nullable=False)
    concept_slug: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    mastery: Mapped[float] = mapped_column(Float, default=0.2, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.2, nullable=False)
    retention: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    learning_velocity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    revision_frequency: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_patterns: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    misconceptions: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    revision_due_turn: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    revision_due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship(back_populates="learner_states")


class QuestionRecord(Base, TimestampMixin):
    __tablename__ = "question_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("learning_sessions.id"), nullable=True)
    concept_slug: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    topic: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    blueprint_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    question_type: Mapped[str] = mapped_column(String(32), default="mcq", nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    options_json: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, default="", nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    bloom_level: Mapped[str] = mapped_column(String(64), default="understand", nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    session: Mapped["LearningSession"] = relationship()
    attempts: Mapped[list["AttemptRecord"]] = relationship(back_populates="question", cascade="all,delete-orphan")


class AttemptRecord(Base, TimestampMixin):
    __tablename__ = "attempt_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("question_records.id"), index=True, nullable=False)
    session_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("learning_sessions.id"), nullable=True)
    user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    mastery_change: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    retention_change: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    misconception: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    question: Mapped["QuestionRecord"] = relationship(back_populates="attempts")
    session: Mapped["LearningSession"] = relationship()


class KnowledgeDocument(Base, TimestampMixin):
    __tablename__ = "knowledge_documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    doc_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(String(64), default="topic", nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
