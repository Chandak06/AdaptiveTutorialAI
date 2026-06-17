from langchain_chroma import Chroma

from adaptive_tutor.rag.embeddings import get_embeddings

from adaptive_tutor.config import (
    QUESTION_MEMORY_PATH,
    QUESTION_MEMORY_COLLECTION,
)


class QuestionMemory:

    def __init__(self):

        self.vectorstore = Chroma(
            collection_name=QUESTION_MEMORY_COLLECTION,
            persist_directory=str(
                QUESTION_MEMORY_PATH
            ),
            embedding_function=get_embeddings(),
        )

    # =====================================
    # Store Generated Question
    # =====================================

    def save_question(
    self,
    question: str,
    metadata: dict | None = None,
    ) -> None:

        metadata = metadata or {}

        self.vectorstore.add_texts(
            texts=[question],
            metadatas=[metadata],
        )

    # =====================================
    # Similar Question Retrieval
    # =====================================

    def retrieve(
        self,
        query,
        k=5,
    ):

        return self.vectorstore.similarity_search(
            query,
            k=k,
        )

    # =====================================
    # Retrieval with Scores
    # =====================================

    def retrieve_with_scores(
        self,
        query,
        k=5,
    ):

        return self.vectorstore.similarity_search_with_score(
            query,
            k=k,
        )

    # =====================================
    # Topic Retrieval
    # =====================================

    def retrieve_topic_questions(
        self,
        topic,
        k=10,
    ):

        return self.vectorstore.similarity_search(
            topic,
            k=k,
        )

    # =====================================
    # Difficulty Retrieval
    # =====================================

    def retrieve_hard_questions(
        self,
        topic,
        k=10,
    ):

        docs = self.vectorstore.similarity_search(
            topic,
            k=25,
        )

        return [
            doc
            for doc in docs
            if doc.metadata.get(
                "difficulty"
            )
            == "Hard"
        ][:k]

    def retrieve_expert_questions(
        self,
        topic,
        k=10,
    ):

        docs = self.vectorstore.similarity_search(
            topic,
            k=25,
        )

        return [
            doc
            for doc in docs
            if doc.metadata.get(
                "difficulty"
            )
            == "Expert"
        ][:k]

    # =====================================
    # Direct Access
    # =====================================

    def get_vectorstore(self) -> Chroma:
        return self.vectorstore