from adaptive_tutor.rag.retriever import (
    get_retriever,
)

from adaptive_tutor.rag.question_retriever import (
    QuestionRetriever,
)

from adaptive_tutor.rag.question_memory import (
    QuestionMemory,
)

memory = QuestionMemory()

question_retriever = QuestionRetriever()


# =====================================================
# Curriculum Retrieval
# =====================================================

def retrieve_context(topic: str) -> str:

    retriever = get_retriever()

    docs = retriever.invoke(topic)

    return "\n".join(
        doc.page_content
        for doc in docs
    )


# =====================================================
# Question Memory Storage
# =====================================================

def store_generated_question(
    question: str,
    metadata: dict | None = None,
) -> None:

    memory.save_question(
        question,
        metadata or {},
    )


# =====================================================
# Similar Question Retrieval
# =====================================================

def retrieve_similar_questions(
    question: str,
    k: int = 5,
):

    return question_retriever.get_related_questions(
        question,
        k=k,
    )


# =====================================================
# Topic Question Retrieval
# =====================================================

def retrieve_topic_questions(
    topic: str,
    k: int = 10,
):

    return question_retriever.get_topic_questions(
        topic,
        k=k,
    )


# =====================================================
# Hard Question Retrieval
# =====================================================

def retrieve_hard_questions(
    topic: str,
    k: int = 5,
):

    return question_retriever.get_hard_questions(
        topic,
        k=k,
    )


# =====================================================
# Expert Question Retrieval
# =====================================================

def retrieve_expert_questions(
    topic: str,
    k: int = 5,
):

    return question_retriever.get_expert_questions(
        topic,
        k=k,
    )


# =====================================================
# RAG Difficulty Agent Context
# =====================================================

def build_hard_question_context(
    question: str,
    k: int = 5,
) -> str:

    docs = retrieve_similar_questions(
        question,
        k=k,
    )

    return "\n\n".join(
        getattr(doc, "page_content", str(doc))
        for doc in docs
    )


# =====================================================
# Question Evolution Context
# =====================================================

def build_question_evolution_context(
    topic: str,
    k: int = 10,
) -> str:

    docs = retrieve_topic_questions(
        topic,
        k=k,
    )

    return "\n\n".join(
        getattr(doc, "page_content", str(doc))
        for doc in docs
    )