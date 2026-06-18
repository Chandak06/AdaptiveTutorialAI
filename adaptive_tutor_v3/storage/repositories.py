from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from storage import models


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db


class UserRepository(BaseRepository):
    def get_by_email(self, email: str):
        stmt = select(models.User).where(models.User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def get(self, user_id: str):
        return self.db.get(models.User, user_id)

    def add(self, user: models.User):
        self.db.add(user)
        return user


class ConceptRepository(BaseRepository):
    def get_by_slug(self, slug: str):
        stmt = select(models.Concept).where(models.Concept.slug == slug)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_by_topic(self, topic: str) -> list[models.Concept]:
        stmt = select(models.Concept).where(models.Concept.topic == topic).order_by(models.Concept.difficulty, models.Concept.name)
        return list(self.db.execute(stmt).scalars().all())

    def upsert_many(self, concepts: Sequence[models.Concept]) -> list[models.Concept]:
        saved = []
        for concept in concepts:
            existing = self.get_by_slug(concept.slug)
            if existing:
                for attr in ("topic", "name", "parent_slug", "difficulty", "prerequisites", "objectives", "metadata_json"):
                    setattr(existing, attr, getattr(concept, attr))
                saved.append(existing)
            else:
                self.db.add(concept)
                saved.append(concept)
        return saved


class LearnerStateRepository(BaseRepository):
    def get(self, user_id: str, concept_slug: str):
        stmt = select(models.LearnerState).where(
            models.LearnerState.user_id == user_id,
            models.LearnerState.concept_slug == concept_slug,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_by_user(self, user_id: str) -> list[models.LearnerState]:
        stmt = select(models.LearnerState).where(models.LearnerState.user_id == user_id)
        return list(self.db.execute(stmt).scalars().all())

    def add(self, state: models.LearnerState):
        self.db.add(state)
        return state


class SessionRepository(BaseRepository):
    def get(self, session_id: str):
        return self.db.get(models.LearningSession, session_id)

    def list_for_user(self, user_id: str):
        stmt = select(models.LearningSession).where(models.LearningSession.user_id == user_id).order_by(models.LearningSession.started_at.desc())
        return list(self.db.execute(stmt).scalars().all())

    def add(self, session: models.LearningSession):
        self.db.add(session)
        return session


class QuestionRepository(BaseRepository):
    def add(self, question: models.QuestionRecord):
        self.db.add(question)
        return question

    def get(self, question_id: str):
        return self.db.get(models.QuestionRecord, question_id)

    def list_for_concept(self, concept_slug: str, limit: int = 20):
        stmt = select(models.QuestionRecord).where(models.QuestionRecord.concept_slug == concept_slug).order_by(models.QuestionRecord.created_at.desc()).limit(limit)
        return list(self.db.execute(stmt).scalars().all())


class AttemptRepository(BaseRepository):
    def add(self, attempt: models.AttemptRecord):
        self.db.add(attempt)
        return attempt

    def list_for_user(self, user_id: str):
        stmt = select(models.AttemptRecord).where(models.AttemptRecord.user_id == user_id).order_by(models.AttemptRecord.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())


class KnowledgeDocumentRepository(BaseRepository):
    def add(self, document: models.KnowledgeDocument):
        self.db.add(document)
        return document

    def list(self, limit: int = 100):
        stmt = select(models.KnowledgeDocument).order_by(models.KnowledgeDocument.created_at.desc()).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def get_by_doc_id(self, doc_id: str):
        stmt = select(models.KnowledgeDocument).where(models.KnowledgeDocument.doc_id == doc_id)
        return self.db.execute(stmt).scalar_one_or_none()
