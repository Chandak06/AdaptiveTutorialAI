# Setup Guide

1. Copy `.env.example` to `.env`.
2. Run `docker-compose up --build`.
3. Open `/docs` in the API container.
4. Seed data is loaded automatically from `data/topics/`.

For local development, run:

```bash
python -m scripts.seed_db
uvicorn main:app --reload
```
