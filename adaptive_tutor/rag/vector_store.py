from langchain_chroma import Chroma
from  adaptive_tutor.rag.embeddings import get_embeddings
from  adaptive_tutor.config import (
    QUESTION_MEMORY_PATH,
    QUESTION_MEMORY_COLLECTION,
)

embeddings = get_embeddings()


class QuestionVectorStore:
    """
    Stores:
    - curriculum chunks
    - generated questions
    - metadata
    """

    def __init__(self):
        self.vectorstore = Chroma(
            collection_name=QUESTION_MEMORY_COLLECTION,
            persist_directory=str(QUESTION_MEMORY_PATH),
            embedding_function=embeddings,
        )

    # =====================================
    # Initial curriculum ingestion
    # =====================================

    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)

    # =====================================
    # Store generated question
    # =====================================

    def add_question(
        self,
        question,
        answer=None,
        topic=None,
        difficulty=None,
        bloom=None,
    ):

        metadata = {
            "topic": topic or "",
            "difficulty": difficulty or "",
            "bloom": bloom or "",
            "answer": answer or "",
            "type": "question",
        }

        self.vectorstore.add_texts(
            texts=[question],
            metadatas=[metadata],
        )

    # =====================================
    # Similar question retrieval
    # =====================================

    def retrieve_similar(
        self,
        query,
        k=5,
    ):

        return self.vectorstore.similarity_search(
            query,
            k=k,
        )

    # =====================================
    # Retrieve with scores
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
    # Topic specific retrieval
    # =====================================

    def retrieve_topic_questions(
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

    # =====================================
    # Access raw store
    # =====================================

    def get_store(self):
        return self.vectorstore


# =================================================
# Existing API compatibility
# =================================================

def create_vector_store(documents):

    store = QuestionVectorStore()

    store.add_documents(documents)

    return store.get_store()