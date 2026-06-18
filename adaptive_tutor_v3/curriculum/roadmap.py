from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RoadmapStep:
    concept_slug: str
    action: str
    reason: str
    recommended_difficulty: int
