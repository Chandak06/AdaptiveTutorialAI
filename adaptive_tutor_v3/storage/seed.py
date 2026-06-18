from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import uuid

from storage import models
from storage.repositories import ConceptRepository, KnowledgeDocumentRepository


@dataclass(slots=True)
class SeedSummary:
    concepts: int
    documents: int


def _slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def load_topic_payloads(topics_dir: Path) -> list[dict]:
    payloads: list[dict] = []
    if not topics_dir.exists():
        return payloads
    for path in sorted(topics_dir.glob("*.json")):
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return payloads


def topic_to_concepts(topic_payload: dict) -> list[models.Concept]:
    topic_name = topic_payload.get("topic_name") or topic_payload.get("topic") or "Unknown Topic"
    topic_slug = topic_payload.get("slug") or _slugify(topic_name)
    concepts: list[models.Concept] = []

    concept_tree = topic_payload.get("concept_tree") or []
    if concept_tree:
        for idx, item in enumerate(concept_tree):
            label = str(item.get("label") or item.get("core") or f"Concept {idx + 1}")
            slug = _slugify(f"{topic_slug}-{label}-{idx}")
            concepts.append(
                models.Concept(
                    id=str(uuid.uuid4()),
                    topic=topic_name,
                    name=label,
                    slug=slug,
                    parent_slug=None,
                    difficulty=1 if str(item.get("difficulty", "easy")).lower() == "easy" else 3,
                    prerequisites=[p for p in item.get("prerequisites", []) if p],
                    objectives=topic_payload.get("learning_objectives", []),
                    metadata_json={"source_slug": topic_slug, "core": item.get("core", "")},
                )
            )
            for jdx, sub in enumerate(item.get("subconcepts", [])[:4]):
                sub_slug = _slugify(f"{slug}-{sub}-{jdx}")
                concepts.append(
                    models.Concept(
                        id=str(uuid.uuid4()),
                        topic=topic_name,
                        name=str(sub),
                        slug=sub_slug,
                        parent_slug=slug,
                        difficulty=2 if jdx < 2 else 3,
                        prerequisites=[label],
                        objectives=topic_payload.get("learning_objectives", []),
                        metadata_json={"source_slug": topic_slug, "core": sub},
                    )
                )
    else:
        concepts_payload = topic_payload.get("concepts") or [topic_name]
        for idx, concept_name in enumerate(concepts_payload):
            slug = _slugify(f"{topic_slug}-{concept_name}-{idx}")
            concepts.append(
                models.Concept(
                    id=str(uuid.uuid4()),
                    topic=topic_name,
                    name=str(concept_name),
                    slug=slug,
                    parent_slug=None,
                    difficulty=1 + min(4, idx // 2),
                    prerequisites=[],
                    objectives=topic_payload.get("learning_objectives", []),
                    metadata_json={"summary": topic_payload.get("summary", ""), "source_slug": topic_slug},
                )
            )
    return concepts


def topic_to_document(topic_payload: dict) -> models.KnowledgeDocument:
    topic_name = topic_payload.get("topic_name") or "Unknown Topic"
    topic_slug = topic_payload.get("slug") or _slugify(topic_name)
    concepts = topic_payload.get("concepts") or []
    objectives = topic_payload.get("learning_objectives") or []
    content = "\n".join(
        [
            f"Topic: {topic_name}",
            f"Summary: {topic_payload.get('summary', '')}",
            f"Concepts: {', '.join(concepts)}",
            f"Objectives: {'; '.join(objectives)}",
        ]
    )
    return models.KnowledgeDocument(
        id=str(uuid.uuid4()),
        doc_id=f"topic::{topic_slug}",
        title=topic_name,
        content=content,
        source_type="topic",
        metadata_json={"slug": topic_slug, "category": topic_payload.get("category", ""), "bank_version": topic_payload.get("bank_version", 1)},
    )


def seed_from_topics(db, topics_dir: Path) -> SeedSummary:
    topic_payloads = load_topic_payloads(topics_dir)
    concept_repo = ConceptRepository(db)
    doc_repo = KnowledgeDocumentRepository(db)

    total_concepts = 0
    total_documents = 0

    for payload in topic_payloads:
        concepts = topic_to_concepts(payload)
        concept_repo.upsert_many(concepts)
        total_concepts += len(concepts)

        doc = doc_repo.get_by_doc_id(f"topic::{payload.get('slug') or _slugify(payload.get('topic_name', 'unknown'))}")
        if doc is None:
            doc_repo.add(topic_to_document(payload))
            total_documents += 1

    db.commit()
    return SeedSummary(concepts=total_concepts, documents=total_documents)
