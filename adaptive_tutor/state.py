from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_analytics_record() -> dict[str, Any]:
    return {
        "questions_attempted": 0,
        "questions_correct": 0,
        "accuracy": 0.0,
        "topics_completed": 0,
        "concepts_mastered": 0,
        "time_spent_seconds": 0.0,
        "learning_streak": 0,
        "best_streak": 0,
        "revision_count": 0,
        "last_interaction_at": None,
    }


def create_empty_session() -> dict[str, Any]:
    return {
        "schema_version": 2,
        "created_at": utc_now_iso(),
        "last_saved_at": utc_now_iso(),
        "current_topic": "",
        "global_turn": 0,
        "topic_order": [],
        "topics": {},
        "analytics": build_analytics_record(),
        "notes": [],
    }


def create_concept_progress(
    concept_id: str,
    concept_name: str,
    level_index: int,
    level_name: str,
) -> dict[str, Any]:
    return {
        "concept_id": concept_id,
        "concept_name": concept_name,
        "level_index": level_index,
        "level_name": level_name,
        "attempts": 0,
        "correct": 0,
        "accuracy": 0.0,
        "mastered": False,
        "revision_needed": False,
        "understanding_evidence": 0,
        "last_question_type": None,
        "last_seen_turn": None,
        "next_revision_turn": None,
    }


def create_topic_state(topic: str, roadmap: dict[str, Any]) -> dict[str, Any]:
    concepts: dict[str, Any] = {}

    for level in roadmap["levels"]:
        for concept in level["concepts"]:
            concepts[concept["id"]] = create_concept_progress(
                concept_id=concept["id"],
                concept_name=concept["name"],
                level_index=level["index"],
                level_name=level["name"],
            )

    analytics = build_analytics_record()
    analytics["topic_name"] = topic

    return {
        "topic": topic,
        "roadmap": deepcopy(roadmap),
        "current_level_index": 0,
        "current_concept_index": 0,
        "highest_level_reached": 0,
        "completed": False,
        "confidence": 0.0,
        "concepts": concepts,
        "weak_areas": [],
        "completed_concepts": [],
        "revision_queue": [],
        "turns_on_topic": 0,
        "conversation": {
            "summary": "",
            "history": [],
        },
        "analytics": analytics,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }


def deep_merge_defaults(target: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(defaults)

    for key, value in target.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = deep_merge_defaults(value, merged[key])
        else:
            merged[key] = value

    return merged
