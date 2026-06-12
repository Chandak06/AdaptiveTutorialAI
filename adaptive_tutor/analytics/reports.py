from __future__ import annotations

from typing import Any


def build_topic_report(topic_state: dict[str, Any]) -> dict[str, Any]:
    levels = topic_state["roadmap"]["levels"]
    current_level = levels[min(topic_state["current_level_index"], len(levels) - 1)]

    return {
        "topic": topic_state["topic"],
        "current_level": current_level["name"],
        "highest_level_reached": topic_state["highest_level_reached"],
        "confidence": topic_state["confidence"],
        "weak_areas": list(topic_state["weak_areas"]),
        "completed_concepts": len(topic_state["completed_concepts"]),
        "revision_queue_size": len(topic_state["revision_queue"]),
        "accuracy": topic_state["analytics"]["accuracy"],
        "learning_streak": topic_state["analytics"]["learning_streak"],
        "completed": topic_state["completed"],
    }


def build_session_report(session: dict[str, Any]) -> dict[str, Any]:
    return {
        "topics_tracked": len(session["topics"]),
        "current_topic": session["current_topic"],
        "questions_attempted": session["analytics"]["questions_attempted"],
        "questions_correct": session["analytics"]["questions_correct"],
        "accuracy": session["analytics"]["accuracy"],
        "topics_completed": session["analytics"]["topics_completed"],
        "concepts_mastered": session["analytics"]["concepts_mastered"],
        "time_spent_seconds": session["analytics"]["time_spent_seconds"],
        "best_streak": session["analytics"]["best_streak"],
    }
