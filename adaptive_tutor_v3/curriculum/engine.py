from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from knowledge_graph.graph import KnowledgeGraph


@dataclass(slots=True)
class LearnerSnapshot:
    mastery: float
    confidence: float
    retention: float
    velocity: float
    misconceptions: list[str]


class CurriculumEngine:
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph

    def next_step(self, learner: LearnerSnapshot, current_concept: str | None = None) -> dict:
        candidate = current_concept or self.graph.entry_concept()
        if learner.retention < 0.45 or learner.confidence < 0.4:
            return {
                "action": "revision",
                "concept": candidate,
                "reason": "low retention or confidence",
                "recommended_difficulty": max(1, int(round(learner.mastery * 5))),
                "next_concept": self.graph.next_concept(candidate),
            }
        if learner.mastery < 0.55:
            return {
                "action": "teach",
                "concept": candidate,
                "reason": "mastery below progression threshold",
                "recommended_difficulty": max(1, int(round(2 + learner.mastery * 4))),
                "next_concept": self.graph.next_concept(candidate),
            }
        next_concept = self.graph.next_concept(candidate)
        return {
            "action": "advance",
            "concept": next_concept or candidate,
            "reason": "progressing to the next prerequisite-safe concept",
            "recommended_difficulty": min(5, int(round(3 + learner.velocity * 10))),
            "next_concept": self.graph.next_concept(next_concept or candidate),
        }

    def coverage_report(self, learner_states: list[dict]) -> dict:
        mastery = [s.get("mastery", 0.0) for s in learner_states]
        return {
            "average_mastery": round(mean(mastery), 4) if mastery else 0.0,
            "covered_concepts": len(learner_states),
        }
