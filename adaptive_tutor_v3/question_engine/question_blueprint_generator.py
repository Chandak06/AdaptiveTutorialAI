from __future__ import annotations

from question_engine.models import QuestionBlueprint


BLOOM_ORDER = ["remember", "understand", "apply", "analyze", "evaluate", "create"]


class QuestionBlueprintGenerator:
    def generate(self, topic: str, concept: dict, objective: str, learner_profile: dict | None = None) -> QuestionBlueprint:
        difficulty = int(concept.get("difficulty", 1))
        confidence = float((learner_profile or {}).get("confidence", 0.5))
        if difficulty <= 1:
            qtype = "mcq"
            bloom = "understand"
            answer_form = "single_best_answer"
        elif difficulty == 2:
            qtype = "mcq"
            bloom = "apply"
            answer_form = "single_best_answer"
        elif difficulty == 3:
            qtype = "scenario"
            bloom = "analyze"
            answer_form = "constructed_response"
        else:
            qtype = "short_answer"
            bloom = "evaluate" if confidence < 0.6 else "create"
            answer_form = "constructed_response"

        misconceptions = [
            "sign error",
            "scope confusion",
            "missing prerequisite",
            "definition inversion",
        ]
        return QuestionBlueprint(
            topic=topic,
            concept_slug=concept["slug"],
            concept_name=concept["name"],
            objective=objective,
            bloom_level=bloom,
            difficulty=max(1, min(5, difficulty + (1 if confidence < 0.4 else 0))),
            question_type=qtype,
            expected_answer_form=answer_form,
            misconception_targets=misconceptions,
        )
