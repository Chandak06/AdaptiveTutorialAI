from __future__ import annotations

import re
from typing import Any


DEFAULT_LEVELS = [
    (
        "Introduction",
        [
            "Definition of {topic}",
            "Why {topic} matters",
            "Real-world intuition for {topic}",
        ],
    ),
    (
        "Fundamentals",
        [
            "Core terminology in {topic}",
            "Basic operations in {topic}",
            "Essential rules of {topic}",
        ],
    ),
    (
        "Internal Working",
        [
            "How {topic} works internally",
            "Common representations of {topic}",
            "Implementation trade-offs in {topic}",
        ],
    ),
    (
        "Complexity Analysis",
        [
            "Time complexity in {topic}",
            "Space complexity in {topic}",
            "Best and worst cases in {topic}",
        ],
    ),
    (
        "Applications",
        [
            "Everyday applications of {topic}",
            "Problem patterns solved by {topic}",
            "When to choose {topic}",
        ],
    ),
    (
        "Coding Problems",
        [
            "Implement {topic}",
            "Debug a {topic}-based solution",
            "Practice problem on {topic}",
        ],
    ),
    (
        "Interview Questions",
        [
            "Conceptual interview question on {topic}",
            "Design interview question on {topic}",
            "Optimization interview question on {topic}",
        ],
    ),
    (
        "University Exam Level",
        [
            "Long answer explanation of {topic}",
            "Dry run problem on {topic}",
            "Algorithm analysis question on {topic}",
        ],
    ),
    (
        "Advanced Problems",
        [
            "Advanced variant of {topic}",
            "Multi-step problem solving with {topic}",
            "Edge cases in {topic}",
        ],
    ),
    (
        "Expert Level",
        [
            "Scalability concerns in {topic}",
            "Concurrent or distributed aspects of {topic}",
            "Research-level extensions of {topic}",
        ],
    ),
]


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return cleaned or "concept"


def build_fallback_roadmap(topic: str) -> dict[str, Any]:
    levels = []

    for index, (name, concepts) in enumerate(DEFAULT_LEVELS):
        normalized_concepts = []
        for concept_text in concepts:
            concept_name = concept_text.format(topic=topic)
            concept_id = f"l{index}-{slugify(concept_name)}"
            normalized_concepts.append(
                {
                    "id": concept_id,
                    "name": concept_name,
                }
            )

        levels.append(
            {
                "index": index,
                "name": name,
                "concepts": normalized_concepts,
            }
        )

    return {
        "topic": topic,
        "levels": levels,
    }


def normalize_roadmap(topic: str, payload: dict[str, Any] | None) -> dict[str, Any]:
    fallback = build_fallback_roadmap(topic)

    if not isinstance(payload, dict):
        return fallback

    raw_levels = payload.get("levels")
    if not isinstance(raw_levels, list):
        return fallback

    normalized_levels = []

    for index in range(len(DEFAULT_LEVELS)):
        fallback_level = fallback["levels"][index]
        generated_level = raw_levels[index] if index < len(raw_levels) else {}
        level_name = generated_level.get("name") or generated_level.get("title")
        if not isinstance(level_name, str) or not level_name.strip():
            level_name = fallback_level["name"]

        raw_concepts = generated_level.get("concepts")
        normalized_concepts = []

        if isinstance(raw_concepts, list):
            for concept in raw_concepts:
                if isinstance(concept, dict):
                    concept_name = concept.get("name")
                else:
                    concept_name = concept

                if not isinstance(concept_name, str):
                    continue

                concept_name = concept_name.strip()
                if not concept_name:
                    continue

                concept_id = f"l{index}-{slugify(concept_name)}"
                normalized_concepts.append(
                    {
                        "id": concept_id,
                        "name": concept_name,
                    }
                )

        if len(normalized_concepts) < 3:
            normalized_concepts = fallback_level["concepts"]
        else:
            normalized_concepts = normalized_concepts[:5]

        normalized_levels.append(
            {
                "index": index,
                "name": level_name,
                "concepts": normalized_concepts,
            }
        )

    return {
        "topic": topic,
        "levels": normalized_levels,
    }


class RoadmapGenerator:
    def __init__(self, llm_client: Any) -> None:
        self.llm_client = llm_client

    def build(self, topic: str) -> dict[str, Any]:
        generated = self.llm_client.generate_roadmap(topic)
        return normalize_roadmap(topic, generated)
