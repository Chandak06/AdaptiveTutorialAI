from __future__ import annotations

from fastapi import FastAPI

from api.routers import analytics, auth, curriculum, evaluation, health, knowledge, questions, rag, sessions, users
from config import settings
from knowledge_graph.service import KnowledgeGraphService
from storage.database import init_db, session_scope
from storage.seed import seed_from_topics


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="3.0.0")

    @app.on_event("startup")
    def _startup() -> None:
        init_db()
        graph_service = KnowledgeGraphService(settings.data_dir / "topics")
        app.state.graph_service = graph_service
        if settings.seed_on_startup:
            with session_scope() as db:
                seed_from_topics(db, settings.data_dir / "topics")

    app.include_router(health.router)
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
    app.include_router(questions.router, prefix="/questions", tags=["questions"])
    app.include_router(curriculum.router, prefix="/curriculum", tags=["curriculum"])
    app.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
    app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
    app.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
    app.include_router(rag.router, prefix="/rag", tags=["rag"])
    return app


app = create_app()
