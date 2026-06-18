from __future__ import annotations

from config import settings
from storage.database import init_db, session_scope
from storage.seed import seed_from_topics


def test_seed_loads_topics():
    init_db()
    with session_scope() as db:
        summary = seed_from_topics(db, settings.data_dir / "topics")
        assert summary.concepts > 0
        assert summary.documents > 0
