from __future__ import annotations

from llm.client import get_llm_client
from rag.retriever import Retriever
from rag.vector_store import HybridVectorStore


class RAGChain:
    def __init__(self, store: HybridVectorStore | None = None):
        self.store = store or HybridVectorStore()
        self.retriever = Retriever(self.store)
        self.llm = get_llm_client()

    def ingest(self, docs: list[dict]) -> None:
        self.store.add_many(docs)

    def answer(self, question: str, metadata_filter: dict | None = None) -> dict:
        context = self.retriever.build_context(question, k=5, metadata_filter=metadata_filter)
        answer = self.llm.generate_answer(question=question, context=context)
        return {
            "question": question,
            "context": context,
            "answer": answer,
            "sources": self.retriever.retrieve(question, k=5, metadata_filter=metadata_filter),
        }
