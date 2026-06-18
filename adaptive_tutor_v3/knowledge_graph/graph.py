from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ConceptNode:
    slug: str
    topic: str
    name: str
    parent_slug: str | None = None
    difficulty: int = 1
    prerequisites: list[str] = field(default_factory=list)
    objectives: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class KnowledgeGraph:
    def __init__(self, nodes: dict[str, ConceptNode] | None = None):
        self.nodes: dict[str, ConceptNode] = nodes or {}
        self.children: dict[str, list[str]] = {}
        for node in self.nodes.values():
            if node.parent_slug:
                self.children.setdefault(node.parent_slug, []).append(node.slug)

    def add_node(self, node: ConceptNode) -> None:
        self.nodes[node.slug] = node
        if node.parent_slug:
            self.children.setdefault(node.parent_slug, []).append(node.slug)

    def get(self, slug: str) -> ConceptNode | None:
        return self.nodes.get(slug)

    def concepts_for_topic(self, topic: str) -> list[ConceptNode]:
        topic_n = topic.lower()
        return [node for node in self.nodes.values() if node.topic.lower() == topic_n or topic_n in node.topic.lower()]

    def entry_concept(self) -> str:
        if not self.nodes:
            return "general-concept"
        ordered = sorted(self.nodes.values(), key=lambda n: (n.difficulty, len(n.prerequisites), n.name))
        return ordered[0].slug

    def next_concept(self, current_slug: str | None) -> str | None:
        if current_slug is None or current_slug not in self.nodes:
            return self.entry_concept() if self.nodes else None
        current = self.nodes[current_slug]
        siblings = self.concepts_for_topic(current.topic)
        ordered = sorted(siblings, key=lambda n: (n.difficulty, n.name))
        for idx, node in enumerate(ordered):
            if node.slug == current_slug and idx + 1 < len(ordered):
                return ordered[idx + 1].slug
        return None

    def prerequisites_met(self, slug: str, mastered: set[str]) -> bool:
        node = self.get(slug)
        if node is None:
            return False
        return all(pr in mastered for pr in node.prerequisites)
