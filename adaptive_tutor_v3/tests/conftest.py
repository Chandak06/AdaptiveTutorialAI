from __future__ import annotations

import os
from pathlib import Path

TEST_DB = Path(__file__).resolve().parent.parent / "test_adaptive_tutor_v3.db"
if TEST_DB.exists():
    TEST_DB.unlink()

os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_DB}")
os.environ.setdefault("SEED_ON_STARTUP", "0")
os.environ.setdefault("USE_SENTENCE_TRANSFORMERS", "0")
os.environ.setdefault("SECRET_KEY", "test-secret")
