from __future__ import annotations

from auth.security import create_token, decode_token, hash_password, verify_password


def test_password_hash_roundtrip():
    hashed = hash_password("StrongPass123!")
    assert verify_password("StrongPass123!", hashed)
    assert not verify_password("wrong", hashed)


def test_token_roundtrip():
    token = create_token("user-123", role="teacher", ttl_minutes=1)
    payload = decode_token(token)
    assert payload.sub == "user-123"
    assert payload.role == "teacher"
