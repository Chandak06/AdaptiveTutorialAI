from __future__ import annotations

from rag.vector_store import HybridVectorStore
from rag.retriever import Retriever


def test_vector_store_retrieves_relevant_chunk():
    store = HybridVectorStore()
    store.add("doc-1", "Variables", "Variables store changing values and support assignment.")
    store.add("doc-2", "Queues", "Queues are FIFO data structures.")
    retriever = Retriever(store)
    chunks = retriever.retrieve("assignment and variables", k=1)
    assert chunks[0].doc_id == "doc-1"
