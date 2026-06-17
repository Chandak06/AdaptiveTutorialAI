from __future__ import annotations

from typing import Any


def detect_misconception(
    correct: bool,
    confidence: float,
) -> bool:
    """
    Detect whether a learner likely has a misconception.

    A misconception is assumed when the learner
    is highly confident but incorrect.
    """

    return (
        not correct
        and confidence >= 60
    )


def update_misconceptions(
    topic_state: dict[str, Any],
    concept_name: str,
    correct: bool,
    confidence: float,
) -> None:

    misconceptions = topic_state.setdefault(
        "misconceptions",
        []
    )

    if detect_misconception(
        correct,
        confidence,
    ):

        if concept_name not in misconceptions:

            misconceptions.append(
                concept_name
            )


def misconception_score(
    topic_state: dict[str, Any],
) -> int:

    misconceptions = topic_state.get(
        "misconceptions",
        []
    )

    return len(misconceptions)


def misconception_topics(
    topic_state: dict[str, Any],
) -> list[str]:

    return topic_state.get(
        "misconceptions",
        []
    )


def clear_misconception(
    topic_state: dict[str, Any],
    concept_name: str,
) -> None:

    misconceptions = topic_state.get(
        "misconceptions",
        []
    )

    if concept_name in misconceptions:

        misconceptions.remove(
            concept_name
        )


def has_misconception(
    topic_state: dict[str, Any],
    concept_name: str,
) -> bool:

    return (
        concept_name
        in topic_state.get(
            "misconceptions",
            []
        )
    )