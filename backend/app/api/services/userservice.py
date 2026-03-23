"""User service — CRUD via SQLAlchemy Core."""
from __future__ import annotations

import hashlib
import json
import secrets
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, func, insert, select, update

from app.api.models.user import PasswordUpdate, User, UserUpdate, UserResponse
from app.db.database import Database
from app.db.tables import users


def _hash_pw(plain: str) -> str:
    salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt.encode(), 600_000)
    return f"{salt}${h.hex()}"


def _verify_pw(plain: str, stored: str) -> bool:
    salt, h = stored.split("$", 1)
    return hashlib.pbkdf2_hmac("sha256", plain.encode(), salt.encode(), 600_000).hex() == h


class UserService:
    """Core user operations — single source of truth for row → model mapping."""

    def __init__(self, db: Database) -> None:
        self.db = db

    # ── helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_user(row: dict[str, Any] | None) -> User | None:
        if not row:
            return None
        meta = row.get("metadata")
        if isinstance(meta, str):
            meta = json.loads(meta)
        return User(
            uuid=row["uuid"] if isinstance(row["uuid"], UUID) else UUID(str(row["uuid"])),
            registered_email=row["registered_email"],
            name=row["name"],
            hash=row.get("hash"),
            pfp=row.get("pfp"),
            access_level=row.get("access_level", "user"),
            metadata=meta or {},
            oauth_provider=row.get("oauth_provider"),
            oauth_id=row.get("oauth_id"),
            email_verified=row.get("email_verified", False),
            is_active=row.get("is_active", True),
            last_login_at=row.get("last_login_at"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    @staticmethod
    def to_response(user: User) -> UserResponse:
        return UserResponse(
            uuid=user.uuid,
            registered_email=user.registered_email,
            name=user.name,
            pfp=user.pfp,
            access_level=user.access_level,
            metadata=user.metadata,
            oauth_provider=user.oauth_provider,
            email_verified=user.email_verified,
            is_active=user.is_active,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
        )

    # ── create ─────────────────────────────────────────────────────────────

    async def admin_create_user(
        self, email: str, name: str, password: str, access_level: str = "user",
    ) -> UserResponse:
        """Admin creation — checks existence, hashes password, returns response."""
        existing = await self.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        user = await self.create_user(email, name, _hash_pw(password), access_level)
        return self.to_response(user)

    async def create_user(
        self, email: str, name: str, hashed_password: str, access_level: str = "user",
    ) -> User:
        stmt = (
            insert(users)
            .values(
                uuid=uuid4(), registered_email=email, name=name,
                hash=hashed_password, access_level=access_level,
                metadata={}, email_verified=False,
            )
            .returning(users)
        )
        row = await self.db.fetch_one(stmt)
        return self._row_to_user(row)

    async def create_user_oauth(
        self, email: str, name: str, oauth_provider: str, oauth_id: str,
        pfp: str | None = None, email_verified: bool = False,
    ) -> User:
        stmt = (
            insert(users)
            .values(
                uuid=uuid4(), registered_email=email, name=name, pfp=pfp,
                access_level="user", metadata={},
                oauth_provider=oauth_provider, oauth_id=oauth_id,
                email_verified=email_verified,
            )
            .returning(users)
        )
        row = await self.db.fetch_one(stmt)
        return self._row_to_user(row)

    # ── read ───────────────────────────────────────────────────────────────

    async def get_by_uuid(self, uuid: UUID) -> User | None:
        stmt = select(users).where(users.c.uuid == uuid)
        return self._row_to_user(await self.db.fetch_one(stmt))

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(users).where(users.c.registered_email == email)
        return self._row_to_user(await self.db.fetch_one(stmt))

    async def get_by_oauth(self, provider: str, oauth_id: str) -> User | None:
        stmt = select(users).where(
            users.c.oauth_provider == provider, users.c.oauth_id == oauth_id,
        )
        return self._row_to_user(await self.db.fetch_one(stmt))

    async def list_users(
        self, designation: str | None = None, access_level: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[User]:
        stmt = select(users).order_by(users.c.created_at.desc())
        if designation:
            stmt = stmt.where(users.c.metadata["designation"].astext == designation)
        if access_level:
            stmt = stmt.where(users.c.access_level == access_level)
        stmt = stmt.limit(limit).offset(offset)
        rows = await self.db.fetch_all(stmt)
        return [self._row_to_user(r) for r in rows]

    async def count_users(
        self, designation: str | None = None, access_level: str | None = None,
    ) -> int:
        stmt = select(func.count().label("count")).select_from(users)
        if designation:
            stmt = stmt.where(users.c.metadata["designation"].astext == designation)
        if access_level:
            stmt = stmt.where(users.c.access_level == access_level)
        row = await self.db.fetch_one(stmt)
        return row["count"] if row else 0

    # ── update ─────────────────────────────────────────────────────────────

    async def update_user(self, uuid: UUID, data: UserUpdate) -> User | None:
        fields: dict[str, Any] = {}
        if data.name is not None:
            fields["name"] = data.name
        if data.pfp is not None:
            fields["pfp"] = data.pfp
        if data.access_level is not None:
            fields["access_level"] = data.access_level
        if data.metadata is not None:
            fields["metadata"] = data.metadata
        if data.email_verified is not None:
            fields["email_verified"] = data.email_verified
        if data.is_active is not None:
            fields["is_active"] = data.is_active
        if not fields:
            return await self.get_by_uuid(uuid)
        stmt = update(users).where(users.c.uuid == uuid).values(**fields).returning(users)
        return self._row_to_user(await self.db.fetch_one(stmt))

    async def update_password(self, uuid: UUID, pw: PasswordUpdate) -> bool:
        user = await self.get_by_uuid(uuid)
        if not user:
            return False
        if user.oauth_provider and not user.hash:
            raise ValueError("Cannot update password for OAuth-only users")
        if not _verify_pw(pw.old_password, user.hash):
            raise ValueError("Incorrect current password")
        if pw.new_password != pw.confirm_password:
            raise ValueError("Passwords do not match")
        if pw.new_password == pw.old_password:
            raise ValueError("New password cannot be same as old password")
        stmt = (
            update(users).where(users.c.uuid == uuid)
            .values(hash=_hash_pw(pw.new_password))
            .returning(users)
        )
        return (await self.db.fetch_one(stmt)) is not None

    async def link_oauth(
        self, uuid: UUID, provider: str, oauth_id: str, pfp: str | None = None,
    ) -> User:
        stmt = (
            update(users).where(users.c.uuid == uuid)
            .values(
                oauth_provider=provider, oauth_id=oauth_id,
                pfp=func.coalesce(users.c.pfp, pfp), email_verified=True,
            )
            .returning(users)
        )
        return self._row_to_user(await self.db.fetch_one(stmt))

    async def update_last_login(self, uuid: UUID) -> None:
        stmt = update(users).where(users.c.uuid == uuid).values(
            last_login_at=datetime.now(timezone.utc),
        )
        await self.db.execute(stmt)

    # ── delete ─────────────────────────────────────────────────────────────

    async def delete_user(self, uuid: UUID) -> bool:
        stmt = delete(users).where(users.c.uuid == uuid).returning(users.c.uuid)
        return (await self.db.fetch_one(stmt)) is not None