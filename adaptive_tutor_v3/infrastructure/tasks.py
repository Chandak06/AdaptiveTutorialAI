from __future__ import annotations

from infrastructure.celery_app import celery_app

if celery_app is not None:
    @celery_app.task
    def rebuild_knowledge_graph():
        return "ok"

    @celery_app.task
    def sync_analytics_snapshot():
        return "ok"
else:  # pragma: no cover
    def rebuild_knowledge_graph():
        return "ok"

    def sync_analytics_snapshot():
        return "ok"
