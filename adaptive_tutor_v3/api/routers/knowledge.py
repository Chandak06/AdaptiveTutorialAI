from __future__ import annotations

from fastapi import APIRouter

from config import settings
from knowledge_graph.service import KnowledgeGraphService

router = APIRouter()


@router.get("/topic/{topic}")
def topic(topic: str):
    return KnowledgeGraphService(settings.data_dir / "topics").topic_summary(topic)


@router.get("/concepts")
def concepts():
    service = KnowledgeGraphService(settings.data_dir / "topics")
    return {
        "count": len(service.graph.nodes),
        "concepts": [
            {
                "slug": node.slug,
                "topic": node.topic,
                "name": node.name,
                "difficulty": node.difficulty,
                "parent_slug": node.parent_slug,
            }
            for node in service.graph.nodes.values()
        ],
    }
