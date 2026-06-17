from __future__ import annotations

from typing import Any


class LearnerProfile:

    def __init__(self):

        self.mastery: dict[str, float] = {}

        self.confidence: dict[str, float] = {}

        self.retention: dict[str, float] = {}

        self.weak_topics: list[str] = []

        self.misconceptions: list[str] = []

        self.question_history: list[dict[str, Any]] = []

        self.difficulty_history: list[int] = []

        self.bloom_history: list[str] = []

        self.completed_topics: list[str] = []

        self.total_questions = 0

        self.correct_answers = 0

    def update_mastery(
        self,
        topic: str,
        score: float,
    ) -> None:

        self.mastery[topic] = round(
            score,
            2,
        )

    def update_confidence(
        self,
        topic: str,
        confidence: float,
    ) -> None:

        self.confidence[topic] = round(
            confidence,
            2,
        )

    def update_retention(
        self,
        topic: str,
        retention: float,
    ) -> None:

        self.retention[topic] = round(
            retention,
            2,
        )

    def add_weak_topic(
        self,
        topic: str,
    ) -> None:

        if topic not in self.weak_topics:
            self.weak_topics.append(
                topic
            )

    def remove_weak_topic(
        self,
        topic: str,
    ) -> None:

        if topic in self.weak_topics:
            self.weak_topics.remove(
                topic
            )

    def add_misconception(
        self,
        concept: str,
    ) -> None:

        if concept not in self.misconceptions:
            self.misconceptions.append(
                concept
            )

    def clear_misconception(
        self,
        concept: str,
    ) -> None:

        if concept in self.misconceptions:
            self.misconceptions.remove(
                concept
            )

    def add_question(
        self,
        question: str,
        difficulty: int = 0,
        bloom_level: str = "",
    ) -> None:

        self.question_history.append(
            {
                "question": question,
                "difficulty": difficulty,
                "bloom": bloom_level,
            }
        )

        self.difficulty_history.append(
            difficulty
        )

        self.bloom_history.append(
            bloom_level
        )

    def record_result(
        self,
        correct: bool,
    ) -> None:

        self.total_questions += 1

        if correct:
            self.correct_answers += 1

    def accuracy(
        self,
    ) -> float:

        if self.total_questions == 0:
            return 0.0

        return round(
            (
                self.correct_answers
                / self.total_questions
            )
            * 100,
            2,
        )

    def average_difficulty(
        self,
    ) -> float:

        if not self.difficulty_history:
            return 0.0

        return round(
            sum(
                self.difficulty_history
            )
            / len(
                self.difficulty_history
            ),
            2,
        )

    def summary(
        self,
    ) -> dict[str, Any]:

        return {
            "accuracy": self.accuracy(),
            "average_difficulty": self.average_difficulty(),
            "weak_topics": self.weak_topics,
            "misconceptions": self.misconceptions,
            "questions_seen": len(
                self.question_history
            ),
        }