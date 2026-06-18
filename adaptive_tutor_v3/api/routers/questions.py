from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import db_session
from config import settings
from knowledge_graph.service import KnowledgeGraphService
from question_engine.pipeline import QuestionPipeline
from storage import models
from storage.database import session_scope

router = APIRouter()


@router.post("/generate")
def generate_question(topic: str, db: Session = Depends(db_session)):
    graph_service = KnowledgeGraphService(settings.data_dir / "topics")
    pipeline = QuestionPipeline(graph_service, db)
    payload = pipeline.generate_for_topic(topic)
    return payload


@router.post("/store")
def store_question(payload: dict, db: Session = Depends(db_session)):
    graph_service = KnowledgeGraphService(settings.data_dir / "topics")
    pipeline = QuestionPipeline(graph_service, db)
    return pipeline.store(payload)
