from langchain_chroma import Chroma

from adaptive_tutor.rag.embeddings import (
    get_embeddings,
)

from adaptive_tutor.config import (
    QUESTION_MEMORY_PATH,
    QUESTION_MEMORY_TOP_K,
    QUESTION_MEMORY_COLLECTION,
)

def get_vectorstore():

    return Chroma(
        collection_name=QUESTION_MEMORY_COLLECTION,
        persist_directory=str(QUESTION_MEMORY_PATH),
        embedding_function=get_embeddings(),
    )


def get_retriever(k=None):

    vectorstore = get_vectorstore()

    return vectorstore.as_retriever(
        search_kwargs={
            "k": k or QUESTION_MEMORY_TOP_K
        }
    )


# ==========================================
# Question Retrieval Agent
# ==========================================

class QuestionRetriever:

    def __init__(self):

        self.vectorstore = get_vectorstore()

    def similar_questions(
        self,
        question,
        k=5,
    ):

        return self.vectorstore.similarity_search(
            question,
            k=k,
        )

    def similar_questions_with_scores(
        self,
        question,
        k=5,
    ):

        return self.vectorstore.similarity_search_with_score(
            question,
            k=k,
        )

    def topic_questions(
        self,
        topic,
        k=10,
    ):

        return self.vectorstore.similarity_search(
            topic,
            k=k,
            filter={
                "type": "question"
            },
        )

    def hard_questions(
        self,
        topic,
        k=5,
    ):

        return self.vectorstore.similarity_search(
            topic,
            k=k,
            filter={
                "difficulty": "Hard"
            },
        )

    def expert_questions(
        self,
        topic,
        k=5,
    ):

        return self.vectorstore.similarity_search(
            topic,
            k=k,
            filter={
                "difficulty": "Expert"
            },
        )

    def misconception_questions(
        self,
        topic,
        k=5,
    ):

        return self.vectorstore.similarity_search(
            topic,
            k=k,
            filter={
                "type": "question"
            },
        )