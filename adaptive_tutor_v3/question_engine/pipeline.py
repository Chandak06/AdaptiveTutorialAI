from __future__ import annotations

import uuid
from dataclasses import asdict
from sqlalchemy.orm import Session

from question_engine.concept_extractor import ConceptExtractor
from question_engine.difficulty_calibrator import DifficultyCalibrator
from question_engine.distractor_generator import DistractorGenerator
from question_engine.objective_generator import ObjectiveGenerator
from question_engine.question_blueprint_generator import QuestionBlueprintGenerator
from question_engine.question_generator import QuestionGenerator
from question_engine.validator import QuestionValidator
from storage import models
from storage.repositories import QuestionRepository
from storage.seed import load_topic_payloads


class QuestionPipeline:
    def __init__(self, graph, db: Session):
        self.graph = graph
        self.db = db
        self.questions = QuestionRepository(db)
        self.extractor = ConceptExtractor()
        self.objectives = ObjectiveGenerator()
        self.blueprints = QuestionBlueprintGenerator()
        self.generator = QuestionGenerator()
        self.distractors = DistractorGenerator()
        self.validator = QuestionValidator()
        self.calibrator = DifficultyCalibrator()

    def _topic_payload(self, topic: str) -> dict | None:
        if hasattr(self.graph, "topics_dir"):
            for payload in load_topic_payloads(self.graph.topics_dir):
                if (payload.get("topic_name") or "").lower() == topic.lower():
                    return payload
        return None

    def generate_for_topic(self, topic: str, learner_profile: dict | None = None) -> dict:
        concepts = self.extractor.extract(topic, self.graph.graph if hasattr(self.graph, "graph") else self.graph)
        concept = concepts[0]
        topic_payload = self._topic_payload(topic)
        objective = self.objectives.generate(topic_payload, concept, concept.get("difficulty", 1))[0]
        blueprint = self.blueprints.generate(topic, concept, objective, learner_profile)
        prompt, correct_answer = self.generator.generate(blueprint, objective, learner_profile)
        blueprint_data = asdict(blueprint)
        distractors = self.distractors.generate(concept["name"], correct_answer, objective, blueprint_data)
        options = [correct_answer] + distractors
        question_payload = {
            "topic": topic,
            "concept_slug": concept["slug"],
            "concept_name": concept["name"],
            "objective": objective,
            "bloom_level": blueprint.bloom_level,
            "difficulty": self.calibrator.calibrate(blueprint_data, prompt, distractors),
            "question_type": blueprint.question_type,
            "prompt": prompt,
            "options": options,
            "correct_answer": correct_answer,
            "explanation": f"The answer follows from the concept '{concept['name']}' and the objective '{objective}'.",
            "metadata": {
                "blueprint": blueprint_data,
                "misconception_targets": blueprint.misconception_targets,
            },
        }
        valid, issues = self.validator.validate(question_payload)
        question_payload["validation"] = {"valid": valid, "issues": issues}
        return question_payload

    def store(self, question_payload: dict, session_id: str | None = None) -> models.QuestionRecord:
        question = models.QuestionRecord(
            id=str(uuid.uuid4()),
            session_id=session_id,
            concept_slug=question_payload["concept_slug"],
            topic=question_payload["topic"],
            blueprint_json=question_payload.get("metadata", {}).get("blueprint", {}),
            question_type=question_payload["question_type"],
            prompt=question_payload["prompt"],
            options_json=question_payload["options"],
            correct_answer=question_payload["correct_answer"],
            explanation=question_payload["explanation"],
            difficulty=int(question_payload["difficulty"]),
            bloom_level=question_payload["bloom_level"],
            metadata_json=question_payload.get("metadata", {}),
        )
        self.questions.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question
