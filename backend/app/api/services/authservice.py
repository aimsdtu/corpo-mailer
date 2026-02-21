"""Authentication service — JWT, password hashing, register, login, Google OAuth, refresh.
Delegates all user CRUD to ``UserService``.  Stateless JWT refresh tokens.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import hashlib
import secrets

import httpx
from jose import JWTError, jwt

from app.api.models.user import UserResponse
from app.api.services.userservice import UserService
from app.core.config import get_settings
from app.core.logging import logger
from app.db.database import Database

settings = get_settings()

class AuthService:
    """Auth flows — register, login (email + Google), refresh.

    All user DB operations go through ``self._users``.
    """

    def __init__(self, db: Database) -> None:
        self.db = db
        self._users = UserService(db)

    @staticmethod
    def hash_password(plain: str) -> str:
        salt = secrets.token_hex(16)
        h = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt.encode(), 600_000)
        return f"{salt}${h.hex()}"

    @staticmethod
    def verify_password(plain: str, stored: str) -> bool:
        salt, h = stored.split("$", 1)
        return hashlib.pbkdf2_hmac("sha256", plain.encode(), salt.encode(), 600_000).hex() == h

    @staticmethod
    def create_access_token(user_id: str, role: str, provider: str, email: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "role": role,
            "provider": provider,
            "email": email,
            "iat": now,
            "exp": now + timedelta(minutes=settings.jwt_access_token_expire_minutes),
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    @staticmethod
    def create_refresh_token(user_id: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=settings.jwt_refresh_token_expire_days),
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    @staticmethod
    def decode_token(token: str) -> dict[str, Any] | None:
        try:
            return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        except JWTError:
            return None

    # ── helpers ───────────────────────────────────────────────────────────

    def _issue_tokens(self, user, provider: str = "email") -> dict[str, Any]:
        """Build access + refresh token pair + UserResponse."""
        return {
            "access_token": self.create_access_token(
                str(user.uuid), user.access_level, provider, user.registered_email,
            ),
            "refresh_token": self.create_refresh_token(str(user.uuid)),
            "user": UserService.to_response(user),
        }

    # ── public API ────────────────────────────────────────────────────────

    async def register(self, email: str, password: str, name: str) -> dict[str, Any]:
        """Register a new user with email + password.

        Returns ``{"access_token", "refresh_token", "user"}``.
        """
        existing = await self._users.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        hashed = self.hash_password(password)
        user = await self._users.create_user(email=email, name=name, hashed_password=hashed)
        logger.info("User registered: %s", email)
        return self._issue_tokens(user)

    async def login_email(self, email: str, password: str) -> dict[str, Any]:
        """Authenticate with email + password."""
        user = await self._users.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is deactivated")

        if user.hash is None:
            raise ValueError("This account uses OAuth login")

        if not self.verify_password(password, user.hash):
            raise ValueError("Invalid email or password")

        await self._users.update_last_login(user.uuid)
        logger.info("User logged in: %s", email)
        return self._issue_tokens(user)

    # ── Google OAuth ──────────────────────────────────────────────────────

    @staticmethod
    def get_google_auth_url() -> str:
        """Construct Google OAuth2 authorization URL."""
        params = (
            f"client_id={settings.google_client_id}"
            f"&redirect_uri={settings.google_redirect_uri}"
            "&response_type=code"
            "&scope=openid%20email%20profile"
            "&access_type=offline"
            "&prompt=consent"
        )
        return f"https://accounts.google.com/o/oauth2/v2/auth?{params}"

    async def login_google(self, code: str) -> dict[str, Any]:
        """Exchange Google auth code → tokens, upsert user, return app tokens."""
        # Exchange code → Google tokens + user info
        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uri": settings.google_redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            if token_resp.status_code != 200:
                raise ValueError(f"Google token exchange failed: {token_resp.status_code}")
            google_tokens = token_resp.json()

            userinfo_resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {google_tokens['access_token']}"},
            )
            if userinfo_resp.status_code != 200:
                raise ValueError("Failed to fetch Google user info")
            info = userinfo_resp.json()

        google_id = info["id"]
        email = info["email"]
        name = info.get("name", email)
        picture = info.get("picture")
        email_verified = info.get("verified_email", False)

        # Existing OAuth user?
        user = await self._users.get_by_oauth("google", google_id)
        if user:
            await self._users.update_last_login(user.uuid)
            return self._issue_tokens(user, provider="google")

        # Existing email account? Link Google identity if email is verified.
        existing = await self._users.get_by_email(email)
        if existing:
            if not email_verified:
                raise ValueError("Cannot link unverified Google email to existing account")
            user = await self._users.link_oauth(existing.uuid, "google", google_id, picture)
            await self._users.update_last_login(user.uuid)
            logger.info("Linked Google OAuth to existing account: %s", email)
            return self._issue_tokens(user, provider="google")

        # Create new OAuth user
        user = await self._users.create_user_oauth(
            email=email,
            name=name,
            oauth_provider="google",
            oauth_id=google_id,
            pfp=picture,
            email_verified=email_verified,
        )
        logger.info("OAuth user created: %s", email)
        return self._issue_tokens(user, provider="google")

    # ── refresh ───────────────────────────────────────────────────────────

    async def refresh(self, raw_refresh: str) -> dict[str, Any]:
        """Decode stateless refresh JWT, issue new token pair."""
        payload = self.decode_token(raw_refresh)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user = await self._users.get_by_uuid(payload["sub"])
        if not user:
            raise ValueError("User not found")

        if not user.is_active:
            raise ValueError("Account is deactivated")

        return {
            "access_token": self.create_access_token(
                str(user.uuid), user.access_level,
                user.oauth_provider or "email", user.registered_email,
            ),
            "refresh_token": self.create_refresh_token(str(user.uuid)),
        }
