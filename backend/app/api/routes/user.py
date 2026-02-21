"""User routes — CRUD with query-param filtering."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies.auth import inject_user, require_role
from app.api.models.user import PasswordUpdate, UserCreate, UserResponse, UserUpdate
from app.api.services.userservice import UserService
from app.db.database import Database
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


def _get_service(db: Database = Depends(get_db)) -> UserService:
    return UserService(db)


def _parse_uuid(raw: str) -> UUID:
    try:
        return UUID(raw)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid UUID format")


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@require_role("admin")
async def create_user(
    body: UserCreate,
    user: dict = Depends(inject_user),
    service: UserService = Depends(_get_service),
):
    try:
        return await service.admin_create_user(
            email=body.registered_email,
            name=body.name,
            password=body.password,
            access_level=body.access_level,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


@router.get("/count", response_model=dict)
@require_role("admin", "moderator")
async def count_users(
    designation: str | None = Query(None),
    access_level: str | None = Query(None),
    user: dict = Depends(inject_user),
    service: UserService = Depends(_get_service),
):
    return {"count": await service.count_users(designation=designation, access_level=access_level)}


@router.get("/{uuid}", response_model=UserResponse)
@require_role("user", "admin", "moderator")
async def get_user(
    uuid: str,
    user: dict = Depends(inject_user),
    service: UserService = Depends(_get_service),
):
    result = await service.get_by_uuid(_parse_uuid(uuid))
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return UserService.to_response(result)


@router.get("", response_model=list[UserResponse])
@require_role("admin", "moderator")
async def list_users(
    designation: str | None = Query(None),
    access_level: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: dict = Depends(inject_user),
    service: UserService = Depends(_get_service),
):
    users = await service.list_users(
        designation=designation, access_level=access_level, limit=limit, offset=offset,
    )
    return [UserService.to_response(u) for u in users]


@router.patch("/{uuid}", response_model=UserResponse)
@require_role("user", "admin", "moderator")
async def update_user(
    uuid: str,
    body: UserUpdate,
    user: dict = Depends(inject_user),
    service: UserService = Depends(_get_service),
):
    result = await service.update_user(_parse_uuid(uuid), body)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return UserService.to_response(result)


@router.put("/{uuid}/password", status_code=status.HTTP_204_NO_CONTENT)
@require_role("user", "admin")
async def update_password(
    uuid: str,
    body: PasswordUpdate,
    user: dict = Depends(inject_user),
    service: UserService = Depends(_get_service),
):
    try:
        if not await service.update_password(_parse_uuid(uuid), body):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.delete("/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
@require_role("admin")
async def delete_user(
    uuid: str,
    user: dict = Depends(inject_user),
    service: UserService = Depends(_get_service),
):
    if not await service.delete_user(_parse_uuid(uuid)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
