from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RetrievedChunk:
    doc_id: str
    title: str
    content: str
    score: float
    metadata: dict = field(default_factory=dict)
