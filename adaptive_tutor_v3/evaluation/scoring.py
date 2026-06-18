from __future__ import annotations

from assessment.normalizer import normalize_text, semantic_match
from learner_model.misconceptions import detect_misconception


def score_correctness(question: dict, answer_text: str) -> tuple[bool, float]:
    correct = question["correct_answer"]
    score = semantic_match(answer_text, correct)
    return score >= 0.85, round(score, 4)


def estimate_confidence(user_confidence: float | None, semantic_score: float, mastery: float) -> float:
    base = user_confidence if user_confidence is not None else 0.5
    confidence = (base * 0.6) + (semantic_score * 0.2) + (mastery * 0.2)
    return max(0.0, min(1.0, round(confidence, 4)))


def infer_misconception(question: dict, answer_text: str, is_correct: bool, confidence: float) -> str:
    if is_correct:
        return ""
    concept = normalize_text(question.get("concept_slug", ""))
    if "fraction" in concept and "/" in answer_text:
        return "fraction addition error"
    if "equation" in concept or "linear" in concept:
        return "algebraic sign error"
    if detect_misconception(is_correct, confidence):
        return f"high-confidence error in {concept or 'concept'}"
    return "conceptual misconception"


def mastery_delta(is_correct: bool, confidence: float, difficulty: int, mastery: float) -> float:
    direction = 1 if is_correct else -1
    base = 0.04 + (difficulty * 0.01)
    confidence_bonus = (confidence - 0.5) * 0.05
    inertia = (1.0 - mastery) * 0.03 if is_correct else mastery * 0.02
    delta = direction * (base + confidence_bonus + inertia)
    return round(max(-0.15, min(0.15, delta)), 4)


def retention_delta(is_correct: bool, confidence: float) -> float:
    delta = (0.03 if is_correct else -0.04) + ((confidence - 0.5) * 0.02)
    return round(max(-0.1, min(0.08, delta)), 4)
