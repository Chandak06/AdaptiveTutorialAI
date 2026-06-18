from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class QuestionBlueprint:
    topic: str
    concept_slug: str
    concept_name: str
    objective: str
    bloom_level: str
    difficulty: int
    question_type: str
    expected_answer_form: str
    misconception_targets: list[str] = field(default_factory=list)


@dataclass(slots=True)
class GeneratedQuestion:
    topic: str
    concept_slug: str
    concept_name: str
    objective: str
    bloom_level: str
    difficulty: int
    question_type: str
    prompt: str
    options: list[str]
    correct_answer: str
    explanation: str
    metadata: dict = field(default_factory=dict)
