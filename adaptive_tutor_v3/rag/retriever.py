from __future__ import annotations

from rag.vector_store import HybridVectorStore


class Retriever:
    def __init__(self, store: HybridVectorStore):
        self.store = store

    def retrieve(self, query: str, k: int = 5, metadata_filter: dict | None = None):
        return self.store.search(query, k=k, metadata_filter=metadata_filter)

    def build_context(self, query: str, k: int = 5, metadata_filter: dict | None = None) -> str:
        chunks = self.retrieve(query, k=k, metadata_filter=metadata_filter)
        return "\n\n".join(f"[{chunk.title}] {chunk.content}" for chunk in chunks)
