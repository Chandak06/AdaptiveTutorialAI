from __future__ import annotations

from typing import Any


TRUE_VALUES = {"true", "t", "1"}
FALSE_VALUES = {"false", "f", "2"}


def normalize_true_false_answer(answer: Any) -> str | None:
    cleaned = str(answer).strip().lower()

    if cleaned in TRUE_VALUES:
        return "True"

    if cleaned in FALSE_VALUES:
        return "False"

    return None


def evaluate_true_false_answer(user_answer: Any, correct_answer: Any) -> dict[str, Any]:
    normalized_user = normalize_true_false_answer(user_answer)
    normalized_correct = normalize_true_false_answer(correct_answer)

    if normalized_correct is None:
        normalized_correct = "True"

    is_correct = normalized_user == normalized_correct
    feedback = (
        "Correct. Your statement classification is solid."
        if is_correct
        else "That one is off. Slow down and test the statement against the core definition."
    )

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "normalized_user_answer": normalized_user,
        "normalized_correct_answer": normalized_correct,
    }
