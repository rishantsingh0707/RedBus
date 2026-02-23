import base64
import binascii
import hashlib
import hmac
import json
import os
import secrets
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any

from exceptions import AppException

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    iterations = 100_000
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    ).hex()
    return f"pbkdf2_sha256${iterations}${salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    if stored_hash.startswith("pbkdf2_sha256$"):
        try:
            _, iterations, salt, digest = stored_hash.split("$", 3)
            computed = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                int(iterations),
            ).hex()
            return hmac.compare_digest(computed, digest)
        except ValueError:
            return False
    return hmac.compare_digest(password, stored_hash)


def create_access_token(
    subject: str, expires_delta: timedelta | None = None, extra_claims: dict | None = None
) -> str:
    if not JWT_SECRET_KEY:
        raise AppException(
            status_code=500,
            code="MISSING_JWT_SECRET",
            message="JWT secret is not configured.",
        )

    now = datetime.now(timezone.utc)
    expire_at = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire_at.timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)

    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    encoded_header = _b64url_encode(
        json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    encoded_payload = _b64url_encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )

    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(
        JWT_SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    encoded_signature = _b64url_encode(signature)
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError as exc:
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid token format.",
        ) from exc

    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    expected_signature = hmac.new(
        JWT_SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    try:
        provided_signature = _b64url_decode(encoded_signature)
    except (ValueError, binascii.Error) as exc:
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid token signature encoding.",
        ) from exc

    if not hmac.compare_digest(expected_signature, provided_signature):
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid token signature.",
        )

    try:
        payload_bytes = _b64url_decode(encoded_payload)
        payload = json.loads(payload_bytes.decode("utf-8"))
    except (ValueError, binascii.Error, json.JSONDecodeError) as exc:
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid token payload.",
        ) from exc

    if not isinstance(payload, dict):
        raise AppException(
            status_code=401,
            code="INVALID_TOKEN",
            message="Invalid token claims.",
        )
    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(datetime.now(timezone.utc).timestamp()):
        raise AppException(
            status_code=401,
            code="TOKEN_EXPIRED",
            message="Token has expired.",
        )
    return payload


def verify_google_id_token(id_token: str) -> dict[str, Any]:
    if not GOOGLE_CLIENT_ID:
        raise AppException(
            status_code=500,
            code="MISSING_GOOGLE_CLIENT_ID",
            message="Google OAuth client ID is not configured.",
        )

    query = urllib.parse.urlencode({"id_token": id_token})
    url = f"https://oauth2.googleapis.com/tokeninfo?{query}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise AppException(
            status_code=401,
            code="GOOGLE_TOKEN_INVALID",
            message="Unable to verify Google token.",
        ) from exc

    aud = payload.get("aud")
    iss = payload.get("iss")
    email_verified = payload.get("email_verified")

    if aud != GOOGLE_CLIENT_ID:
        raise AppException(
            status_code=401,
            code="GOOGLE_AUDIENCE_MISMATCH",
            message="Google token audience is invalid.",
        )

    if iss not in {"accounts.google.com", "https://accounts.google.com"}:
        raise AppException(
            status_code=401,
            code="GOOGLE_ISSUER_INVALID",
            message="Google token issuer is invalid.",
        )

    if str(email_verified).lower() != "true":
        raise AppException(
            status_code=401,
            code="GOOGLE_EMAIL_NOT_VERIFIED",
            message="Google email is not verified.",
        )

    return payload
