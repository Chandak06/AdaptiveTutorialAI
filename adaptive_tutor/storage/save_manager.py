from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from adaptive_tutor.config import SESSION_PATH
from adaptive_tutor.state import (
    create_empty_session,
    utc_now_iso,
)


class SaveManager:

    def __init__(
        self,
        path: Path | None = None,
    ) -> None:

        self.path = path or SESSION_PATH

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _normalize_session(
        self,
        session: dict[str, Any],
    ) -> dict[str, Any]:

        defaults = create_empty_session()

        for key, value in defaults.items():

            session.setdefault(
                key,
                value,
            )

        session.setdefault(
            "schema_version",
            3,
        )

        session.setdefault(
            "topics",
            {},
        )

        session.setdefault(
            "topic_order",
            [],
        )

        session.setdefault(
            "notes",
            [],
        )

        session.setdefault(
            "analytics",
            defaults["analytics"],
        )

        for topic_state in session[
            "topics"
        ].values():

            topic_state.setdefault(
                "misconceptions",
                [],
            )

            topic_state.setdefault(
                "difficulty_history",
                [],
            )

            topic_state.setdefault(
                "generated_question_count",
                0,
            )

            topic_state.setdefault(
                "revision_queue",
                [],
            )

            topic_state.setdefault(
                "weak_areas",
                [],
            )

            topic_state.setdefault(
                "completed_concepts",
                [],
            )

        return session

    def load_session(
        self,
    ) -> dict[str, Any]:

        if not self.path.exists():

            session = (
                create_empty_session()
            )

            self.save_session(
                session
            )

            return session

        try:

            raw_text = (
                self.path.read_text(
                    encoding="utf-8"
                ).strip()
            )

        except OSError:

            session = (
                create_empty_session()
            )

            session["notes"].append(
                "Unable to read previous session."
            )

            self.save_session(
                session
            )

            return session

        if not raw_text:

            session = (
                create_empty_session()
            )

            self.save_session(
                session
            )

            return session

        try:

            session = json.loads(
                raw_text
            )

        except json.JSONDecodeError:

            backup_path = (
                self.path.with_suffix(
                    ".corrupt.json"
                )
            )

            try:

                backup_path.write_text(
                    raw_text,
                    encoding="utf-8",
                )

            except OSError:
                pass

            session = (
                create_empty_session()
            )

            session["notes"].append(
                f"Corrupted session recovered on {utc_now_iso()}."
            )

            self.save_session(
                session
            )

            return session

        if not isinstance(
            session,
            dict,
        ):
            session = (
                create_empty_session()
            )

        session = self._normalize_session(
            session
        )

        if not session.get(
            "created_at"
        ):
            session[
                "created_at"
            ] = utc_now_iso()

        if not session.get(
            "last_saved_at"
        ):
            session[
                "last_saved_at"
            ] = utc_now_iso()

        return session

    def save_session(
        self,
        session: dict[str, Any],
    ) -> None:

        session = self._normalize_session(
            session
        )

        session[
            "last_saved_at"
        ] = utc_now_iso()

        serialized = json.dumps(
            session,
            indent=2,
            ensure_ascii=False,
        )

        self.path.write_text(
            serialized,
            encoding="utf-8",
        )