from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import sqrt
import re
from typing import Iterable

from rag.documents import RetrievedChunk


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


@dataclass(slots=True)
class EmbeddedDocument:
    doc_id: str
    title: str
    content: str
    metadata: dict
    vector: dict[str, float]


class SentenceEmbeddingBackend:
    def __init__(self):
        self.model = None
        try:
            import os
            if os.getenv("USE_SENTENCE_TRANSFORMERS", "0") == "1":
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            self.model = None

    def embed(self, text: str) -> dict[str, float]:
        if self.model is not None:
            vec = self.model.encode([text], normalize_embeddings=True)[0]
            return {str(i): float(v) for i, v in enumerate(vec)}
        counts = Counter(_tokens(text))
        total = sum(counts.values()) or 1
        return {term: count / total for term, count in counts.items()}


class HybridVectorStore:
    def __init__(self):
        self.backend = SentenceEmbeddingBackend()
        self.documents: dict[str, EmbeddedDocument] = {}

    def add(self, doc_id: str, title: str, content: str, metadata: dict | None = None) -> None:
        metadata = metadata or {}
        self.documents[doc_id] = EmbeddedDocument(
            doc_id=doc_id,
            title=title,
            content=content,
            metadata=metadata,
            vector=self.backend.embed(f"{title}\n{content}"),
        )

    def add_many(self, docs: Iterable[dict]) -> None:
        for doc in docs:
            self.add(doc["doc_id"], doc["title"], doc["content"], doc.get("metadata", {}))

    def _cosine(self, left: dict[str, float], right: dict[str, float]) -> float:
        shared = set(left) & set(right)
        numerator = sum(left[k] * right[k] for k in shared)
        left_norm = sqrt(sum(v * v for v in left.values()))
        right_norm = sqrt(sum(v * v for v in right.values()))
        if not left_norm or not right_norm:
            return 0.0
        return numerator / (left_norm * right_norm)

    def search(self, query: str, k: int = 5, metadata_filter: dict | None = None) -> list[RetrievedChunk]:
        query_vec = self.backend.embed(query)
        scored: list[RetrievedChunk] = []
        for doc in self.documents.values():
            if metadata_filter:
                if any(doc.metadata.get(key) != value for key, value in metadata_filter.items()):
                    continue
            score = self._cosine(query_vec, doc.vector)
            lexical = len(set(_tokens(query)) & set(_tokens(doc.content + " " + doc.title))) / max(1, len(set(_tokens(query))))
            final_score = round((score * 0.7) + (lexical * 0.3), 4)
            scored.append(RetrievedChunk(doc.doc_id, doc.title, doc.content, final_score, dict(doc.metadata)))
        return sorted(scored, key=lambda x: x.score, reverse=True)[:k]


class VectorStoreFactory:
    @staticmethod
    def create():
        return HybridVectorStore()
