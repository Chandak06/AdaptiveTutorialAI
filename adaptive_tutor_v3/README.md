# AdaptiveTutorAI v3

A clean-architecture adaptive tutoring platform with:

- concept-level learner modeling
- curriculum planning and spaced revision
- misconception-aware question generation
- structured evaluation
- hybrid RAG
- analytics for learners and teachers
- FastAPI + PostgreSQL + Redis + Celery + Qdrant

## Quick start

```bash
docker-compose up --build
```

Then open:

- API: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## Seed data

The repository includes topic datasets in `data/topics/` extracted from the earlier projects and normalized for the new question engine and knowledge graph.

## Design

See `docs/` for diagrams, API details, setup, deployment, and developer guidance.
