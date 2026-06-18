from __future__ import annotations

from config import settings
from knowledge_graph.service import KnowledgeGraphService
from question_engine.distractor_generator import DistractorGenerator
from question_engine.pipeline import QuestionPipeline
from question_engine.validator import QuestionValidator
from storage.database import init_db, session_scope
from users.service import UserService


def test_misconception_based_fraction_distractors():
    distractors = DistractorGenerator().generate("Fraction Addition", "7/6", "Add fractions with unlike denominators")
    assert distractors == ["3/5", "2/5", "1"]


def test_question_pipeline_generates_valid_question():
    init_db()
    with session_scope() as db:
        graph = KnowledgeGraphService(settings.data_dir / "topics")
        pipeline = QuestionPipeline(graph, db)
        payload = pipeline.generate_for_topic("Variables", {"mastery": 0.3, "confidence": 0.4})
        valid, issues = QuestionValidator().validate(payload)
        assert valid, issues
        assert len(payload["options"]) == 4
        assert payload["concept_slug"]
        assert payload["objective"]
