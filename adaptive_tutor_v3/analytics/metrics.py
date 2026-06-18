from __future__ import annotations

from statistics import mean


def mastery_trend(states: list[dict]) -> list[dict]:
    ordered = sorted(states, key=lambda s: s.get("updated_at", ""))
    trend = []
    running = []
    for state in ordered:
        running.append(float(state.get("mastery", 0.0)))
        trend.append({"concept_slug": state.get("concept_slug", ""), "rolling_mastery": round(mean(running), 4)})
    return trend


def learning_velocity(states: list[dict]) -> float:
    if not states:
        return 0.0
    return round(mean(float(s.get("learning_velocity", 0.0)) for s in states), 4)


def retention_curve(states: list[dict]) -> list[float]:
    return [round(float(s.get("retention", 0.0)), 4) for s in sorted(states, key=lambda s: s.get("retention", 0.0), reverse=True)]


def misconception_heatmap(states: list[dict]) -> dict[str, int]:
    heatmap: dict[str, int] = {}
    for state in states:
        for m in state.get("misconceptions", []):
            heatmap[m] = heatmap.get(m, 0) + 1
    return heatmap
