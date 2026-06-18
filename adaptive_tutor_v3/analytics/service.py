from __future__ import annotations

from statistics import mean

from analytics.metrics import learning_velocity, mastery_trend, misconception_heatmap, retention_curve


class AnalyticsService:
    def student_analytics(self, learner_states: list[dict], attempts: list[dict]) -> dict:
        mastery = [float(s.get("mastery", 0.0)) for s in learner_states]
        confidence = [float(s.get("confidence", 0.0)) for s in learner_states]
        return {
            "mastery_average": round(mean(mastery), 4) if mastery else 0.0,
            "confidence_average": round(mean(confidence), 4) if confidence else 0.0,
            "learning_velocity": learning_velocity(learner_states),
            "retention_curve": retention_curve(learner_states),
            "mastery_trend": mastery_trend(learner_states),
            "attempt_count": len(attempts),
        }

    def teacher_analytics(self, learner_states: list[dict], concept_catalog: list[dict]) -> dict:
        weaknesses = sorted(learner_states, key=lambda s: (s.get("mastery", 0.0), s.get("retention", 0.0)))[:10]
        return {
            "class_weaknesses": [s.get("concept_slug", "") for s in weaknesses],
            "misconception_heatmap": misconception_heatmap(learner_states),
            "curriculum_effectiveness": round(mean(s.get("mastery", 0.0) for s in learner_states), 4) if learner_states else 0.0,
            "concept_coverage": len(concept_catalog),
        }
