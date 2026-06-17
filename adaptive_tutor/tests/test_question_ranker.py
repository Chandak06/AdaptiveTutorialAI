from adaptive_tutor.assessment.question_ranker import (
    QuestionRanker,
)


def test_ranker():

    ranker = QuestionRanker()

    result = ranker.rank(
        "Explain DFS traversal."
    )

    assert "difficulty" in result