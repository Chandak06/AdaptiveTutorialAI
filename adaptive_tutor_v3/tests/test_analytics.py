from __future__ import annotations

from analytics.metrics import learning_velocity, mastery_trend, misconception_heatmap, retention_curve


def test_analytics_helpers():
    states = [
        {"concept_slug": "a", "mastery": 0.2, "confidence": 0.3, "retention": 0.4, "learning_velocity": 0.1, "misconceptions": ["m1"], "updated_at": "2024-01-01"},
        {"concept_slug": "b", "mastery": 0.6, "confidence": 0.7, "retention": 0.8, "learning_velocity": 0.2, "misconceptions": ["m1", "m2"], "updated_at": "2024-01-02"},
    ]
    assert learning_velocity(states) == 0.15
    assert len(mastery_trend(states)) == 2
    assert misconception_heatmap(states)["m1"] == 2
    assert retention_curve(states)[0] == 0.8
