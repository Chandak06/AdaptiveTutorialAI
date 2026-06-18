from __future__ import annotations

from question_engine.models import GeneratedQuestion


class QuestionGenerator:
    def generate(self, blueprint, objective: str, learner_profile: dict | None = None) -> tuple[str, str]:
        concept = blueprint.concept_name
        if blueprint.question_type == "mcq":
            prompt = f"Which statement about {concept} best supports the objective '{objective}'?"
            answer = f"The key idea of {concept} as it relates to {objective}."
        elif blueprint.question_type == "scenario":
            prompt = f"A learner is applying {concept} in a new scenario. What is the best next step to satisfy the objective '{objective}'?"
            answer = f"Apply {concept} by connecting the scenario back to the objective."
        else:
            prompt = f"Explain how {concept} helps achieve the objective '{objective}'."
            answer = f"{concept} helps because it directly supports {objective}."
        return prompt, answer
