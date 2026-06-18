from __future__ import annotations

from fastapi.testclient import TestClient

from api.app import create_app


def test_health_and_auth_flow():
    app = create_app()
    with TestClient(app) as client:
        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"

        register = client.post(
            "/auth/register",
            json={"email": "api@example.com", "password": "StrongPass123!", "full_name": "API User", "role": "learner"},
        )
        assert register.status_code == 200, register.text

        login = client.post(
            "/auth/login",
            json={"email": "api@example.com", "password": "StrongPass123!"},
        )
        assert login.status_code == 200, login.text
        assert "access_token" in login.json()
