"""User domain models.

- ``User``            — full DB row (internal, never serialised to clients)
- ``UserResponse``    — safe projection for API responses
- ``UserCreate``      — admin-created user payload
- ``UserCreateOAuth`` — OAuth-based registration (no password)
- ``UserUpdate``      — partial update payload (COALESCE-friendly)
- ``PasswordUpdate``  — password change
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Literal, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Internal DB model
# ---------------------------------------------------------------------------


class User(BaseModel):
    """Full user row — never return this directly to clients."""

    uuid: UUID
    registered_email: EmailStr
    name: str
    hash: Optional[str] = None
    pfp: Optional[str] = None
    access_level: Literal["user", "admin", "moderator", "superuser"] = "user"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    oauth_provider: Optional[Literal["google", "microsoft", "github"]] = None
    oauth_id: Optional[str] = None
    email_verified: bool = False
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# API response
# ---------------------------------------------------------------------------


class UserResponse(BaseModel):
    """Safe projection for API responses — excludes hash."""

    uuid: UUID
    registered_email: EmailStr
    name: str
    pfp: Optional[str] = None
    access_level: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    oauth_provider: Optional[str] = None
    email_verified: bool = False
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Create payloads
# ---------------------------------------------------------------------------


class UserCreate(BaseModel):
    """Admin-created user (password is plaintext, hashed server-side)."""

    registered_email: EmailStr
    name: str
    password: str = Field(..., min_length=8)
    access_level: Literal["user", "admin", "moderator", "superuser"] = "user"


class UserCreateOAuth(BaseModel):
    """OAuth-based registration (no password)."""

    registered_email: EmailStr
    name: str
    pfp: Optional[str] = None
    oauth_provider: Literal["google", "microsoft", "github"]
    oauth_id: str
    email_verified: bool = False
    access_level: Literal["user", "admin", "moderator", "superuser"] = "user"


# ---------------------------------------------------------------------------
# Update payloads
# ---------------------------------------------------------------------------


class UserUpdate(BaseModel):
    """Partial update — None fields are skipped via COALESCE."""

    name: Optional[str] = None
    pfp: Optional[str] = None
    access_level: Optional[Literal["user", "admin", "moderator", "superuser"]] = None
    metadata: Optional[Dict[str, Any]] = None
    email_verified: Optional[bool] = None
    is_active: Optional[bool] = None


class PasswordUpdate(BaseModel):
    """Password change — both fields are plaintext, verified + hashed server-side."""

    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)