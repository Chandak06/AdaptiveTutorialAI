from __future__ import annotations

from typing import Any

from adaptive_tutor.config import (
    MASTERY_ACCURACY_THRESHOLD,
    MIN_MASTERY_ATTEMPTS,
)


HIGH_SIGNAL_QUESTION_TYPES = {
    "fill_blank",
    "short_answer",
    "one_liner",
    "scenario",
    "coding",
    "long_form",
    "exam_style",
    "problem_solving",
    "expert_reasoning",
}


def refresh_topic_lists(topic_state: dict[str, Any]) -> None:
    weak_areas = []
    completed = []

    for concept in topic_state["concepts"].values():

        if concept["mastered"]:
            completed.append(
                concept["concept_name"]
            )

        elif concept["revision_needed"]:
            weak_areas.append(
                concept["concept_name"]
            )

    topic_state["weak_areas"] = sorted(
        dict.fromkeys(weak_areas)
    )

    topic_state["completed_concepts"] = sorted(
        dict.fromkeys(completed)
    )


def recalculate_confidence(
    topic_state: dict[str, Any]
) -> float:

    analytics = topic_state["analytics"]

    total_concepts = max(
        1,
        len(topic_state["concepts"])
    )

    mastered_count = sum(
        1
        for concept in topic_state["concepts"].values()
        if concept["mastered"]
    )

    difficulty_history = topic_state.get(
        "difficulty_history",
        []
    )

    avg_difficulty = (
        sum(difficulty_history)
        / len(difficulty_history)
        if difficulty_history
        else 0
    )

    accuracy_component = (
        analytics["accuracy"] * 0.35
    )

    mastery_component = (
        mastered_count
        / total_concepts
    ) * 25.0

    streak_component = min(
        analytics["learning_streak"],
        10,
    ) * 2.0

    difficulty_component = (
        topic_state["highest_level_reached"]
        / 9.0
    ) * 15.0

    challenge_component = (
        avg_difficulty / 100.0
    ) * 15.0

    topic_state["confidence"] = round(
        min(
            100.0,
            accuracy_component
            + mastery_component
            + streak_component
            + difficulty_component
            + challenge_component,
        ),
        2,
    )

    return topic_state["confidence"]


def update_concept_mastery(
    topic_state: dict[str, Any],
    concept_id: str,
    is_correct: bool,
    question_type: str,
) -> dict[str, Any]:

    concept = topic_state["concepts"][
        concept_id
    ]

    mastered_before = concept[
        "mastered"
    ]

    concept["attempts"] += 1

    concept[
        "last_question_type"
    ] = question_type

    if is_correct:
        concept["correct"] += 1

    concept["accuracy"] = round(
        (
            concept["correct"]
            / concept["attempts"]
        )
        * 100.0,
        2,
    )

    if is_correct and (
        question_type
        in HIGH_SIGNAL_QUESTION_TYPES
        or concept["level_index"] >= 2
    ):
        concept[
            "understanding_evidence"
        ] += 1

    if not is_correct:

        concept[
            "revision_needed"
        ] = True

        misconceptions = topic_state.setdefault(
            "misconceptions",
            []
        )

        if (
            concept["concept_name"]
            not in misconceptions
        ):
            misconceptions.append(
                concept["concept_name"]
            )

    concept["mastered"] = (
        concept["accuracy"]
        >= MASTERY_ACCURACY_THRESHOLD
        and concept["attempts"]
        >= MIN_MASTERY_ATTEMPTS
        and concept[
            "understanding_evidence"
        ] >= 1
    )

    if concept["mastered"]:

        concept[
            "revision_needed"
        ] = False

        concept[
            "next_revision_turn"
        ] = None

    refresh_topic_lists(
        topic_state
    )

    recalculate_confidence(
        topic_state
    )

    return {
        "concept": concept,
        "mastered_now": (
            concept["mastered"]
            and not mastered_before
        ),
    }