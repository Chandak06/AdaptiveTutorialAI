from __future__ import annotations


class ObjectiveGenerator:
    def generate(self, topic_payload: dict | None, concept: dict, difficulty: int) -> list[str]:
        base = list((topic_payload or {}).get("learning_objectives") or [])
        if base:
            return base[:3]
        name = concept["name"]
        return [
            f"Explain the core idea of {name}.",
            f"Apply {name} in a short scenario.",
            f"Distinguish {name} from a common misconception.",
        ]
