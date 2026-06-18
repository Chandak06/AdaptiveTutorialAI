from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import db_session
from config import settings
from curriculum.engine import CurriculumEngine
from knowledge_graph.service import KnowledgeGraphService
from recommendation.engine import RecommendationEngine

router = APIRouter()


@router.get("/recommendation")
def recommendation(user_mastery: float = 0.2, confidence: float = 0.2, retention: float = 0.5, velocity: float = 0.0, current_concept: str | None = None):
    graph_service = KnowledgeGraphService(settings.data_dir / "topics")
    engine = CurriculumEngine(graph_service.graph)
    recommendation_engine = RecommendationEngine(engine)
    learner_state = {
        "mastery": user_mastery,
        "confidence": confidence,
        "retention": retention,
        "learning_velocity": velocity,
        "misconceptions": [],
    }
    return recommendation_engine.recommend(learner_state, current_concept=current_concept)
