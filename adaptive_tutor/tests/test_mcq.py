from adaptive_tutor.evaluation.mcq import (
    evaluate_mcq_answer,
)


def test_mcq_correct():

    result = evaluate_mcq_answer(
        "A",
        "A",
        [
            "A",
            "B",
            "C",
            "D",
        ],
    )

    assert result["is_correct"]