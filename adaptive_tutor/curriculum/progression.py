from __future__ import annotations

from typing import Any

from adaptive_tutor.config import QUESTION_TYPE_LADDER


class ProgressionEngine:
    def __init__(self, revision_scheduler: Any) -> None:
        self.revision_scheduler = revision_scheduler

    def sync_position(self, topic_state: dict[str, Any]) -> None:
        levels = topic_state["roadmap"]["levels"]
        level_index = topic_state.get("current_level_index", 0)
        concept_index = topic_state.get("current_concept_index", 0)

        while level_index < len(levels):
            concepts = levels[level_index]["concepts"]

            while concept_index < len(concepts):
                concept_id = concepts[concept_index]["id"]
                if not topic_state["concepts"][concept_id]["mastered"]:
                    topic_state["current_level_index"] = level_index
                    topic_state["current_concept_index"] = concept_index
                    topic_state["highest_level_reached"] = max(
                        topic_state["highest_level_reached"],
                        level_index,
                    )
                    return
                concept_index += 1

            level_index += 1
            concept_index = 0

        topic_state["completed"] = True
        topic_state["current_level_index"] = max(0, len(levels) - 1)
        topic_state["current_concept_index"] = 0
        topic_state["highest_level_reached"] = max(
            topic_state["highest_level_reached"],
            len(levels) - 1,
        )

    def _select_question_type(
        self,
        concept_state: dict[str, Any],
        level_index: int,
        mode: str,
    ) -> str:
        ladder = QUESTION_TYPE_LADDER.get(level_index, ["short_answer"])
        step = min(concept_state["attempts"], len(ladder) - 1)

        if mode == "revision" and len(ladder) > 1:
            step = max(step, 1)

        return ladder[step]

    def _build_target(
        self,
        topic_state: dict[str, Any],
        concept_id: str,
        mode: str,
    ) -> dict[str, Any]:
        concept_state = topic_state["concepts"][concept_id]
        question_type = self._select_question_type(
            concept_state=concept_state,
            level_index=concept_state["level_index"],
            mode=mode,
        )

        return {
            "mode": mode,
            "concept_id": concept_state["concept_id"],
            "concept_name": concept_state["concept_name"],
            "level_index": concept_state["level_index"],
            "level_name": concept_state["level_name"],
            "question_type": question_type,
        }

    def next_target(
        self,
        topic_state: dict[str, Any],
        current_turn: int,
    ) -> dict[str, Any] | None:
        self.sync_position(topic_state)

        if topic_state["completed"]:
            return None

        revision_target = self.revision_scheduler.next_due_concept(
            topic_state=topic_state,
            current_turn=current_turn,
        )

        if revision_target:
            return self._build_target(
                topic_state=topic_state,
                concept_id=revision_target,
                mode="revision",
            )

        level = topic_state["roadmap"]["levels"][topic_state["current_level_index"]]
        concept = level["concepts"][topic_state["current_concept_index"]]

        return self._build_target(
            topic_state=topic_state,
            concept_id=concept["id"],
            mode="core",
        )
