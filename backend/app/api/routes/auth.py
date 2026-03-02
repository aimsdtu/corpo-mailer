"""Auth routes — register, login (email + Google OAuth), refresh, logout, me.

All token logic is delegated to ``AuthService``.
Routes handle HTTP concerns only: cookies, status codes, responses.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi.responses import RedirectResponse

from app.api.dependencies.auth import inject_user, require_role
from app.api.models.auth import (
    LoginRequest,
    MeResponse,
    RefreshResponse,
    RegisterRequest,
    TokenResponse,
)
from app.api.services.authservice import AuthService
from app.db.database import Database
from app.db.session import get_db
from app.core.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["auth"])

_COOKIE = "refresh_token"
_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 days


def _get_service(db: Database = Depends(get_db)) -> AuthService:
    return AuthService(db)


# ── Register ──────────────────────────────────────────────────────────────


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, response: Response, svc: AuthService = Depends(_get_service)):
    try:
        result = await svc.register(email=body.email, password=body.password, name=body.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    response.set_cookie(_COOKIE, result["refresh_token"], httponly=True, samesite="lax", max_age=_COOKIE_AGE, path="/api/v1/auth")
    return TokenResponse(access_token=result["access_token"], user=result["user"])


# ── Login (email + password) ─────────────────────────────────────────────


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, response: Response, svc: AuthService = Depends(_get_service)):
    try:
        result = await svc.login_email(body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    response.set_cookie(_COOKIE, result["refresh_token"], httponly=True, samesite="lax", max_age=_COOKIE_AGE, path="/api/v1/auth")
    return TokenResponse(access_token=result["access_token"], user=result["user"])


# ── Google OAuth ──────────────────────────────────────────────────────────


@router.get("/login/google")
async def login_google():
    """Redirect user to Google consent screen."""
    url = AuthService.get_google_auth_url()
    return RedirectResponse(url)


@router.get("/callback/google", response_model=TokenResponse)
async def callback_google(
    code: str = Query(...),
    response: Response = Response(),
    svc: AuthService = Depends(_get_service),
):
    """Handle Google OAuth callback — exchange code, create/login user."""
    try:
        result = await svc.login_google(code)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    redirect = RedirectResponse(
        url=f"{settings.frontend_origin}/oauth/callback?access_token={result['access_token']}",
        status_code=status.HTTP_302_FOUND,
    )
    redirect.set_cookie(
        _COOKIE,
        result["refresh_token"],
        httponly=True,
        samesite="lax",
        max_age=_COOKIE_AGE,
        path="/api/v1/auth",
    )
    return redirect


# ── Refresh ───────────────────────────────────────────────────────────────


@router.post("/refresh", response_model=RefreshResponse)
async def refresh(request: Request, response: Response, svc: AuthService = Depends(_get_service)):
    raw = request.cookies.get(_COOKIE)
    if not raw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")

    try:
        result = await svc.refresh(raw)
    except ValueError as e:
        response.delete_cookie(_COOKIE, path="/api/v1/auth")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    response.set_cookie(_COOKIE, result["refresh_token"], httponly=True, samesite="lax", max_age=_COOKIE_AGE, path="/api/v1/auth")
    return RefreshResponse(access_token=result["access_token"])


# ── Logout ────────────────────────────────────────────────────────────────


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(_COOKIE, path="/api/v1/auth")


# ── Me ────────────────────────────────────────────────────────────────────


@router.get("/me", response_model=MeResponse)
@require_role("user", "admin", "moderator", "superuser")
async def me(user: dict = Depends(inject_user)):
    return MeResponse(sub=user["sub"], role=user["role"], provider=user["provider"], email=user["email"])
