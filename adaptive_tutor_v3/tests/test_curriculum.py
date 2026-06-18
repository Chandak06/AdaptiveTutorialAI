from __future__ import annotations

from curriculum.engine import CurriculumEngine, LearnerSnapshot
from knowledge_graph.service import KnowledgeGraphService
from config import settings


def test_curriculum_prefers_revision_when_retention_is_low():
    graph = KnowledgeGraphService(settings.data_dir / "topics").graph
    engine = CurriculumEngine(graph)
    decision = engine.next_step(
        LearnerSnapshot(mastery=0.7, confidence=0.3, retention=0.2, velocity=0.0, misconceptions=[]),
        current_concept=None,
    )
    assert decision["action"] == "revision"
