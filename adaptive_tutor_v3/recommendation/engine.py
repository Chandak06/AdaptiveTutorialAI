from __future__ import annotations

from curriculum.engine import CurriculumEngine, LearnerSnapshot
from revision_engine.scheduler import SpacedRevisionScheduler


class RecommendationEngine:
    def __init__(self, curriculum_engine: CurriculumEngine):
        self.curriculum = curriculum_engine
        self.scheduler = SpacedRevisionScheduler()

    def recommend(self, learner_state: dict, current_concept: str | None = None) -> dict:
        snapshot = LearnerSnapshot(
            mastery=float(learner_state.get("mastery", 0.2)),
            confidence=float(learner_state.get("confidence", 0.2)),
            retention=float(learner_state.get("retention", 0.5)),
            velocity=float(learner_state.get("learning_velocity", 0.0)),
            misconceptions=list(learner_state.get("misconceptions", [])),
        )
        next_step = self.curriculum.next_step(snapshot, current_concept=current_concept)
        revision = self.scheduler.schedule(
            concept_slug=next_step["concept"],
            mastery=snapshot.mastery,
            retention=snapshot.retention,
            error_count=len(snapshot.misconceptions),
        )
        return {
            "curriculum": next_step,
            "revision": {
                "concept_slug": revision.concept_slug,
                "due_at": revision.due_at.isoformat(),
                "interval_days": revision.interval_days,
                "reason": revision.reason,
            },
        }
