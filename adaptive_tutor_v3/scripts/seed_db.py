from __future__ import annotations

from config import settings
from storage.database import init_db, session_scope
from storage.seed import seed_from_topics


def main() -> None:
    init_db()
    with session_scope() as db:
        summary = seed_from_topics(db, settings.data_dir / "topics")
        print(f"Seeded {summary.concepts} concepts and {summary.documents} documents.")


if __name__ == "__main__":
    main()
