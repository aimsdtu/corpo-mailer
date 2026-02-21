"""Auth domain models — request/response shapes for authentication endpoints."""
from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from app.api.models.user import UserResponse

class RegisterRequest(BaseModel):
    """Minimal registration — profile details added later via PATCH /users/{uuid}."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str

class LoginRequest(BaseModel):
    """Email + password login."""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Returned on successful login / register."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class RefreshResponse(BaseModel):
    """Returned on successful token refresh."""
    access_token: str
    token_type: str = "bearer"

class MeResponse(BaseModel):
    """Decoded JWT claims returned by ``GET /auth/me``."""
    sub: str
    role: str
    provider: str
    email: str
