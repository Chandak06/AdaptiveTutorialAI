from __future__ import annotations

import os

try:
    from celery import Celery
except Exception:  # pragma: no cover
    Celery = None


def create_celery_app():
    if Celery is None:
        return None
    app = Celery(
        "adaptive_tutor_v3",
        broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
        backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    )
    app.conf.task_serializer = "json"
    app.conf.result_serializer = "json"
    app.conf.accept_content = ["json"]
    return app


celery_app = create_celery_app()
