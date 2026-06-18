from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from config import settings


@dataclass(slots=True)
class TokenPayload:
    sub: str
    exp: int
    role: str = "learner"


def _derive_key(secret: str) -> bytes:
    return hashlib.sha256(secret.encode("utf-8")).digest()


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000)
    return f"{salt}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, expected = password_hash.split("$", 1)
    except ValueError:
        return False
    check = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 120_000).hex()
    return hmac.compare_digest(check, expected)


def create_token(user_id: str, role: str = "learner", ttl_minutes: int | None = None) -> str:
    expires = datetime.now(tz=timezone.utc) + timedelta(minutes=ttl_minutes or settings.token_ttl_minutes)
    payload = json.dumps({"sub": user_id, "exp": int(expires.timestamp()), "role": role}, separators=(",", ":")).encode("utf-8")
    body = base64.urlsafe_b64encode(payload).decode("ascii")
    signature = hmac.new(_derive_key(settings.secret_key), body.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{body}.{signature}"


def decode_token(token: str) -> TokenPayload:
    body, signature = token.split(".", 1)
    expected = hmac.new(_derive_key(settings.secret_key), body.encode("ascii"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise ValueError("Invalid token signature")
    payload = json.loads(base64.urlsafe_b64decode(body.encode("ascii")).decode("utf-8"))
    if int(payload["exp"]) < int(datetime.now(tz=timezone.utc).timestamp()):
        raise ValueError("Token expired")
    return TokenPayload(sub=str(payload["sub"]), exp=int(payload["exp"]), role=str(payload.get("role", "learner")))
