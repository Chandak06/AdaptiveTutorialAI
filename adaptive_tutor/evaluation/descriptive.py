from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

try:
    from rapidfuzz import fuzz
except ImportError:  # pragma: no cover - optional dependency fallback
    fuzz = None


def _normalize_text(text: Any) -> str:
    lowered = str(text).strip().lower()
    lowered = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return " ".join(lowered.split())


def _similarity(left: str, right: str) -> float:
    if fuzz is not None:
        return float(fuzz.token_set_ratio(left, right))
    return SequenceMatcher(None, left, right).ratio() * 100.0


def _keywords_from_context(
    concept_name: str,
    correct_answer: str,
    rubric: list[str],
) -> set[str]:
    source = " ".join([concept_name, correct_answer, " ".join(rubric)])
    normalized = _normalize_text(source)
    return {
        token
        for token in normalized.split()
        if len(token) >= 3
    }


def _local_grade(
    concept_name: str,
    correct_answer: str,
    user_answer: str,
    rubric: list[str],
) -> dict[str, Any]:
    normalized_user = _normalize_text(user_answer)
    normalized_correct = _normalize_text(correct_answer)

    if not normalized_user:
        return {
            "is_correct": False,
            "feedback": "I need at least a short explanation to judge your understanding.",
            "score": 0,
        }

    keyword_pool = _keywords_from_context(concept_name, correct_answer, rubric)
    matched_keywords = [
        keyword
        for keyword in keyword_pool
        if keyword in normalized_user
    ]
    keyword_ratio = (
        len(matched_keywords) / len(keyword_pool)
        if keyword_pool
        else 0.0
    )
    similarity = _similarity(normalized_user, normalized_correct)
    score = round((similarity * 0.7) + (keyword_ratio * 30.0), 2)

    is_correct = (
        similarity >= 70
        or keyword_ratio >= 0.35
        or len(matched_keywords) >= 3
    )
    feedback = (
        "Good explanation. You captured the main idea."
        if is_correct
        else "You are partway there, but your answer is missing key ideas from the concept."
    )

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "score": score,
    }


def evaluate_descriptive_answer(
    question: dict[str, Any],
    user_answer: str,
    llm_client: Any | None = None,
) -> dict[str, Any]:
    local_result = _local_grade(
        concept_name=question.get("concept_name", ""),
        correct_answer=question.get("answer", ""),
        user_answer=user_answer,
        rubric=question.get("rubric", []),
    )

    if llm_client is None:
        return local_result

    llm_result = llm_client.grade_descriptive(
        question=question,
        user_answer=user_answer,
    )

    if llm_result is None:
        return local_result

    if local_result["is_correct"] and not llm_result["is_correct"]:
        if local_result["score"] >= 80:
            return local_result
        llm_result["feedback"] = (
            f"{llm_result['feedback']} I still noticed some relevant understanding in your answer."
        )

    return llm_result
