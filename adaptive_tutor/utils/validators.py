from __future__ import annotations


def validate_score(
    score: float,
) -> float:

    return max(
        0.0,
        min(
            100.0,
            float(score),
        ),
    )


def validate_confidence(
    confidence: float,
) -> float:

    return max(
        0.0,
        min(
            100.0,
            float(confidence),
        ),
    )