from __future__ import annotations

from knowledge_graph.graph import KnowledgeGraph


class ConceptExtractor:
    def extract(self, topic: str, graph: KnowledgeGraph, max_concepts: int = 3) -> list[dict]:
        matches = graph.concepts_for_topic(topic)
        if not matches:
            return [
                {
                    "slug": f"{topic.lower().replace(' ', '-')}-core",
                    "name": topic.title(),
                    "topic": topic,
                    "difficulty": 1,
                    "objectives": [],
                }
            ]
        ordered = sorted(matches, key=lambda n: (n.difficulty, len(n.prerequisites), n.name))
        return [
            {
                "slug": node.slug,
                "name": node.name,
                "topic": node.topic,
                "difficulty": node.difficulty,
                "objectives": node.objectives,
                "metadata": node.metadata,
            }
            for node in ordered[:max_concepts]
        ]
