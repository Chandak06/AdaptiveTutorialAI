from adaptive_tutor.evaluation.true_false import (
    evaluate_true_false_answer,
)


def test_true_false():

    result = evaluate_true_false_answer(
        "True",
        "True",
    )

    assert result["is_correct"]