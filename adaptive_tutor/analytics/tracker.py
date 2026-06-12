from __future__ import annotations

from typing import Any

from adaptive_tutor.curriculum.mastery import recalculate_confidence
from adaptive_tutor.state import utc_now_iso


class AnalyticsTracker:
    def _update_accuracy(self, analytics: dict[str, Any]) -> None:
        attempted = analytics["questions_attempted"]
        correct = analytics["questions_correct"]
        analytics["accuracy"] = round((correct / attempted) * 100.0, 2) if attempted else 0.0

    def sync(self, session: dict[str, Any]) -> None:
        overall = session["analytics"]
        overall["topics_completed"] = sum(
            1 for topic in session["topics"].values() if topic["completed"]
        )
        overall["concepts_mastered"] = sum(
            1
            for topic in session["topics"].values()
            for concept in topic["concepts"].values()
            if concept["mastered"]
        )
        self._update_accuracy(overall)

        for topic_state in session["topics"].values():
            topic_analytics = topic_state["analytics"]
            topic_analytics["topics_completed"] = 1 if topic_state["completed"] else 0
            topic_analytics["concepts_mastered"] = len(topic_state["completed_concepts"])
            self._update_accuracy(topic_analytics)
            recalculate_confidence(topic_state)

    def record_interaction(
        self,
        session: dict[str, Any],
        topic_state: dict[str, Any],
        elapsed_seconds: float,
        is_correct: bool,
        was_revision: bool,
    ) -> None:
        now = utc_now_iso()

        for analytics in (session["analytics"], topic_state["analytics"]):
            analytics["questions_attempted"] += 1
            analytics["time_spent_seconds"] = round(
                analytics["time_spent_seconds"] + max(0.0, elapsed_seconds),
                2,
            )
            analytics["last_interaction_at"] = now

            if is_correct:
                analytics["questions_correct"] += 1
                analytics["learning_streak"] += 1
                analytics["best_streak"] = max(
                    analytics["best_streak"],
                    analytics["learning_streak"],
                )
            else:
                analytics["learning_streak"] = 0

            if was_revision:
                analytics["revision_count"] += 1

            self._update_accuracy(analytics)

        self.sync(session)
