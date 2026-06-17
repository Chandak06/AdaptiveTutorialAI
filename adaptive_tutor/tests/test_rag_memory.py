from adaptive_tutor.rag.question_memory import (
    QuestionMemory,
)


def test_rag_memory():

    memory = QuestionMemory()

    memory.save_question(
        "What is DFS?"
    )

    docs = memory.retrieve(
        "DFS"
    )

    assert len(docs) > 0