from __future__ import annotations


def answer_rubric(question_type: str) -> dict:
    question_type = question_type.lower()
    if question_type == "mcq":
        return {"criteria": ["exact option match", "misconception detection"]}
    if question_type == "short_answer":
        return {"criteria": ["key concept terms", "semantic similarity"]}
    return {"criteria": ["structured reasoning", "conceptual correctness"]}
