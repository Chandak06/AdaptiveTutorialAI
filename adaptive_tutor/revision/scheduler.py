from __future__ import annotations

from typing import Any

from adaptive_tutor.config import (
    MASTERY_ACCURACY_THRESHOLD,
    REVISION_COOLDOWN_TURNS,
)

from adaptive_tutor.curriculum.mastery import (
    refresh_topic_lists,
)


class RevisionScheduler:

    def schedule(
        self,
        topic_state: dict[str, Any],
        concept_id: str,
        current_turn: int,
        is_correct: bool,
    ) -> None:

        concept = topic_state[
            "concepts"
        ][concept_id]

        if concept["mastered"]:

            self.clear(
                topic_state,
                concept_id,
            )

            return

        should_schedule = (

            not is_correct

            or (

                concept["attempts"] >= 2

                and concept["accuracy"]
                < MASTERY_ACCURACY_THRESHOLD

            )
        )

        if not should_schedule:

            if (
                concept["accuracy"]
                >= MASTERY_ACCURACY_THRESHOLD
            ):
                self.clear(
                    topic_state,
                    concept_id,
                )

            return

        confidence = topic_state.get(
            "confidence",
            0,
        )

        cooldown = (
            max(
                1,
                REVISION_COOLDOWN_TURNS - 1,
            )
            if confidence < 50
            else REVISION_COOLDOWN_TURNS
        )

        due_turn = (
            current_turn
            + cooldown
        )

        concept[
            "revision_needed"
        ] = True

        concept[
            "next_revision_turn"
        ] = due_turn

        misconceptions = set(
            topic_state.get(
                "misconceptions",
                [],
            )
        )

        priority = 0

        if (
            concept["concept_name"]
            in misconceptions
        ):
            priority = 2

        elif not is_correct:
            priority = 1

        queue = topic_state[
            "revision_queue"
        ]

        for item in queue:

            if (
                item["concept_id"]
                == concept_id
            ):

                item[
                    "due_turn"
                ] = due_turn

                item[
                    "priority"
                ] = priority

                item[
                    "reason"
                ] = (
                    "accuracy_drop"
                    if is_correct
                    else "incorrect_answer"
                )

                break

        else:

            queue.append(
                {
                    "concept_id": concept_id,
                    "due_turn": due_turn,
                    "priority": priority,
                    "reason": (
                        "accuracy_drop"
                        if is_correct
                        else "incorrect_answer"
                    ),
                }
            )

        queue.sort(
            key=lambda item: (
                item["due_turn"],
                -item.get(
                    "priority",
                    0,
                ),
                item["concept_id"],
            )
        )

        refresh_topic_lists(
            topic_state
        )

    def clear(
        self,
        topic_state: dict[str, Any],
        concept_id: str,
    ) -> None:

        topic_state[
            "revision_queue"
        ] = [

            item

            for item in topic_state[
                "revision_queue"
            ]

            if (
                item["concept_id"]
                != concept_id
            )
        ]

        concept = topic_state[
            "concepts"
        ][concept_id]

        concept[
            "revision_needed"
        ] = False

        concept[
            "next_revision_turn"
        ] = None

        refresh_topic_lists(
            topic_state
        )

    def next_due_concept(
        self,
        topic_state: dict[str, Any],
        current_turn: int,
    ) -> str | None:

        queue = sorted(

            topic_state[
                "revision_queue"
            ],

            key=lambda item: (
                item["due_turn"],
                -item.get(
                    "priority",
                    0,
                ),
            ),
        )

        for item in queue:

            concept = topic_state[
                "concepts"
            ].get(
                item["concept_id"]
            )

            if (
                not concept
                or concept["mastered"]
            ):
                continue

            if (
                item["due_turn"]
                <= current_turn
            ):
                return item[
                    "concept_id"
                ]

        return None