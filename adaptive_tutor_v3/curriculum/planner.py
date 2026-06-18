from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CurriculumDecision:
    concept_slug: str
    action: str
    reason: str
    recommended_difficulty: int
    next_concept: str | None = None
