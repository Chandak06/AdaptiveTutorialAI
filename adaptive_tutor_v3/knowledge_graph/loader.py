from __future__ import annotations

from pathlib import Path
import json

from knowledge_graph.graph import ConceptNode, KnowledgeGraph


def _slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def load_graph_from_topics(topics_dir: Path) -> KnowledgeGraph:
    graph = KnowledgeGraph()
    if not topics_dir.exists():
        return graph

    for path in sorted(topics_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        topic = payload.get("topic_name") or payload.get("topic") or path.stem
        topic_slug = payload.get("slug") or _slugify(topic)
        objectives = payload.get("learning_objectives") or []
        concept_tree = payload.get("concept_tree") or []

        if concept_tree:
            for idx, item in enumerate(concept_tree):
                label = str(item.get("label") or item.get("core") or f"Concept {idx + 1}")
                slug = _slugify(f"{topic_slug}-{label}-{idx}")
                graph.add_node(
                    ConceptNode(
                        slug=slug,
                        topic=topic,
                        name=label,
                        parent_slug=None,
                        difficulty=1 if str(item.get("difficulty", "easy")).lower() == "easy" else 3,
                        prerequisites=[],
                        objectives=list(objectives),
                        metadata={"core": item.get("core", ""), "source_file": path.name},
                    )
                )
                for sub_idx, sub in enumerate(item.get("subconcepts", [])[:5]):
                    sub_slug = _slugify(f"{slug}-{sub}-{sub_idx}")
                    graph.add_node(
                        ConceptNode(
                            slug=sub_slug,
                            topic=topic,
                            name=str(sub),
                            parent_slug=slug,
                            difficulty=2 if sub_idx < 2 else 4,
                            prerequisites=[label],
                            objectives=list(objectives),
                            metadata={"core": str(sub), "source_file": path.name},
                        )
                    )
        else:
            concepts = payload.get("concepts") or [topic]
            for idx, concept in enumerate(concepts):
                slug = _slugify(f"{topic_slug}-{concept}-{idx}")
                graph.add_node(
                    ConceptNode(
                        slug=slug,
                        topic=topic,
                        name=str(concept),
                        difficulty=1 + min(4, idx // 2),
                        prerequisites=[],
                        objectives=list(objectives),
                        metadata={"summary": payload.get("summary", ""), "source_file": path.name},
                    )
                )
    return graph
