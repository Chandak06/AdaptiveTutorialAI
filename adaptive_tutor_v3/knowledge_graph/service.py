from __future__ import annotations

from pathlib import Path

from knowledge_graph.loader import load_graph_from_topics


class KnowledgeGraphService:
    def __init__(self, topics_dir: Path):
        self.topics_dir = topics_dir
        self.graph = load_graph_from_topics(topics_dir)

    def reload(self):
        self.graph = load_graph_from_topics(self.topics_dir)
        return self.graph

    def topic_summary(self, topic: str) -> dict:
        concepts = self.graph.concepts_for_topic(topic)
        return {
            "topic": topic,
            "concept_count": len(concepts),
            "concepts": [
                {
                    "slug": node.slug,
                    "name": node.name,
                    "difficulty": node.difficulty,
                    "parent_slug": node.parent_slug,
                }
                for node in concepts[:50]
            ],
        }
