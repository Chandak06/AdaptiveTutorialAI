from adaptive_tutor.evaluation.semantic import (
    semantic_score,
)


def test_semantic():

    score = semantic_score(
        "Binary Search Tree",
        "Binary Search Tree",
    )

    assert score > 90