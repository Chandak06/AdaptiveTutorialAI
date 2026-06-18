from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(slots=True)
class RevisionPlan:
    concept_slug: str
    due_at: datetime
    interval_days: int
    reason: str


class SpacedRevisionScheduler:
    def next_interval_days(self, mastery: float, retention: float, error_count: int) -> int:
        base = 1 + int((mastery * 6) + (retention * 4))
        penalty = min(4, error_count)
        return max(1, min(21, base - penalty))

    def schedule(self, concept_slug: str, mastery: float, retention: float, error_count: int) -> RevisionPlan:
        interval_days = self.next_interval_days(mastery, retention, error_count)
        reason = "reinforce weak retention" if retention < 0.45 else "spaced review"
        return RevisionPlan(
            concept_slug=concept_slug,
            due_at=datetime.utcnow() + timedelta(days=interval_days),
            interval_days=interval_days,
            reason=reason,
        )
