from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_embeddings():
    """
    Singleton embedding model.

    Used by:
    - Curriculum RAG
    - Question Memory
    - Similar Question Retrieval
    - Misconception Mining
    - Difficulty Generation
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={
            "normalize_embeddings": True
        }
    )