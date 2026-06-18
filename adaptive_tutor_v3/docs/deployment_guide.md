# Deployment Guide

- Use `docker-compose` for local deployment.
- Set `DATABASE_URL`, `REDIS_URL`, and `QDRANT_URL` in production.
- Set a strong `SECRET_KEY`.
- Configure a real LLM provider with `LLM_PROVIDER=openai|anthropic|gemini` and the matching API key.
