from __future__ import annotations

from sentence_transformers import (
    SentenceTransformer,
    util,
)


_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def semantic_score(
    student_answer: str,
    reference_answer: str,
) -> float:

    if (
        not student_answer
        or not reference_answer
    ):
        return 0.0

    emb1 = _model.encode(
        student_answer,
        convert_to_tensor=True,
    )

    emb2 = _model.encode(
        reference_answer,
        convert_to_tensor=True,
    )

    similarity = util.cos_sim(
        emb1,
        emb2,
    )

    return round(
        float(similarity) * 100,
        2,
    )


def evaluate_semantic_answer(
    student_answer: str,
    reference_answer: str,
) -> dict:

    score = semantic_score(
        student_answer,
        reference_answer,
    )

    is_correct = score >= 70

    misconception = (
        score < 50
        and len(
            student_answer.strip()
        ) > 10
    )

    feedback = (
        "Your answer is semantically close to the reference answer."
        if is_correct
        else (
            "Your answer differs significantly from the expected explanation."
        )
    )

    return {
        "is_correct": is_correct,
        "score": score,
        "confidence": score,
        "misconception": misconception,
        "feedback": feedback,
    }