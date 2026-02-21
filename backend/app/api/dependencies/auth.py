"""Auth dependencies — JWT extraction + role-based access decorator.

``inject_user``   — FastAPI dependency that decodes the Bearer token.
``require_role``  — Route decorator that checks the ``role`` claim.

Usage::

    @router.get("/admin/dashboard")
    @require_role("admin")
    async def admin_dashboard(user: dict = Depends(inject_user)):
        ...
"""
from __future__ import annotations

import functools
import inspect
from typing import Any, Callable
from fastapi import HTTPException, Request, status
from app.api.services.authservice import AuthService


# FastAPI dependency — extracts & verifies JWT
async def inject_user(request: Request) -> dict[str, Any]:
    """Decode the access token from the ``Authorization`` header."""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = AuthService.decode_token(auth_header.split(" ", 1)[1])
    if not payload or payload.get("type") == "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# Route-level decorator — verifies role claim

def require_role(*allowed_roles: str) -> Callable:
    """Decorator that enforces role-based access on a route handler.

    Must be used together with ``Depends(inject_user)`` so that the
    ``user`` keyword argument is available at call time.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            user: dict[str, Any] | None = kwargs.get("user")
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )

            user_role = user.get("role", "")
            if user_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Role '{user_role}' does not have access. "
                           f"Required: {', '.join(allowed_roles)}",
                )

            return await func(*args, **kwargs)

        wrapper.__signature__ = inspect.signature(func)
        return wrapper

    return decorator
