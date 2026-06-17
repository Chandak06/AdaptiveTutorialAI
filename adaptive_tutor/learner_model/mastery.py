from __future__ import annotations

from typing import Optional


def update_mastery(
    old_score: float,
    quiz_score: float,
    difficulty_score: Optional[float] = None,
) -> float:
    """
    Update learner mastery score.

    Parameters
    ----------
    old_score : float
        Previous mastery score (0-100)

    quiz_score : float
        Latest assessment score (0-100)

    difficulty_score : float | None
        Difficulty of the attempted question (0-100)

    Returns
    -------
    float
        Updated mastery score
    """

    mastery = (
        old_score * 0.7
        + quiz_score * 0.3
    )

    if difficulty_score is not None:

        bonus = (
            difficulty_score / 100.0
        ) * 5.0

        mastery += bonus

    mastery = max(
        0.0,
        min(
            100.0,
            round(mastery, 2),
        ),
    )

    return mastery


def mastery_level(
    score: float,
) -> str:

    if score >= 90:
        return "Expert"

    if score >= 75:
        return "Advanced"

    if score >= 60:
        return "Intermediate"

    if score >= 40:
        return "Beginner"

    return "Novice"


def needs_revision(
    mastery_score: float,
) -> bool:

    return mastery_score < 60