"""API v1 router — aggregates all resource routers under /api/v1."""
from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router
from app.api.routes.group import router as group_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(group_router)
