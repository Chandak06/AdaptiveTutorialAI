from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

try:
    from rapidfuzz import fuzz
except ImportError:
    fuzz = None


OPTION_LETTERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]


def _clean(
    text: Any,
) -> str:

    return " ".join(
        str(text)
        .strip()
        .lower()
        .split()
    )


def _similarity(
    left: str,
    right: str,
) -> float:

    if fuzz is not None:

        return float(
            fuzz.token_set_ratio(
                left,
                right,
            )
        )

    return (
        SequenceMatcher(
            None,
            left,
            right,
        ).ratio()
        * 100.0
    )


def normalize_mcq_answer(
    answer: Any,
    options: list[str],
) -> str | None:

    if not isinstance(
        answer,
        str,
    ):
        answer = str(answer)

    cleaned = _clean(answer)

    if not cleaned:
        return None

    if cleaned.isdigit():

        index = int(cleaned) - 1

        if (
            0 <= index
            < len(options)
        ):
            return options[index]

    if (
        len(cleaned) == 1
        and cleaned.upper()
        in OPTION_LETTERS[: len(options)]
    ):

        index = OPTION_LETTERS.index(
            cleaned.upper()
        )

        return options[index]

    for option in options:

        if _clean(option) == cleaned:
            return option

    scored_options = [

        (
            _similarity(
                cleaned,
                _clean(option),
            ),
            option,
        )

        for option in options
    ]

    best_score, best_option = max(
        scored_options,
        default=(0, None),
    )

    if best_score >= 85:
        return best_option

    return None


def evaluate_mcq_answer(
    user_answer: Any,
    correct_answer: Any,
    options: list[str],
) -> dict[str, Any]:

    normalized_user = (
        normalize_mcq_answer(
            user_answer,
            options,
        )
    )

    normalized_correct = (
        normalize_mcq_answer(
            correct_answer,
            options,
        )
    )

    if (
        normalized_correct is None
        and options
    ):
        normalized_correct = options[0]

    is_correct = (
        normalized_user
        == normalized_correct
    )

    confidence = (
        100.0
        if normalized_user
        else 0.0
    )

    misconception = (
        normalized_user is not None
        and not is_correct
    )

    feedback = (
        "Nice work. You picked the right option."
        if is_correct
        else (
            "Not quite. Recheck the concept and compare the options carefully."
        )
    )

    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "score": (
            100.0
            if is_correct
            else 0.0
        ),
        "confidence": confidence,
        "misconception": misconception,
        "normalized_user_answer": normalized_user,
        "normalized_correct_answer": normalized_correct,
    }