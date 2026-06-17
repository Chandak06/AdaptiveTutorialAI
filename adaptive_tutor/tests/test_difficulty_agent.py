from adaptive_tutor.assessment.difficulty_agent import (
    DifficultyAgent,
)


def test_difficulty_agent():

    agent = DifficultyAgent()

    result = agent.generate_hard_question(
        topic="Graphs",
        context="DFS"
    )

    assert result