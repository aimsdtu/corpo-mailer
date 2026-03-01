from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.auth import inject_user, require_role
from app.api.models.group import (
    GroupCreate,
    GroupUpdate,
    GroupMemberUpdate,
    GroupResponse,
    GroupMemberResponse,
)
from app.api.services.groupservice import GroupService
from app.db.database import Database
from app.db.session import get_db


router = APIRouter(prefix="/groups", tags=["groups"])


# -------------------------------------------------------------------
# Dependency
# -------------------------------------------------------------------

def _get_service(db: Database = Depends(get_db)) -> GroupService:
    return GroupService(db)


# -------------------------------------------------------------------
# My Groups (must come before /{group_id})
# -------------------------------------------------------------------


@router.get("/me/groups", response_model=list[GroupResponse])
async def my_groups(
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    return await service.get_user_groups(
        UUID(user["sub"])
    )


# -------------------------------------------------------------------
# Groups
# -------------------------------------------------------------------


@router.post("", response_model=GroupResponse)
@require_role("admin", "superuser")
async def create_group(
    body: GroupCreate,
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    return await service.create_group(
        body.name,
        body.bio,
        UUID(user["sub"]),
    )


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: UUID,
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    # Ensure user belongs to this group
    role = await service.get_member_role(group_id, UUID(user["sub"]))
    if not role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this group",
        )

    group = await service.get_group(group_id)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )

    return group


@router.get("", response_model=list[GroupResponse])
async def list_groups(
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    # Non-admin users should only see groups they belong to
    if user["role"] in ("admin", "superuser"):
        return await service.list_groups()
    return await service.get_user_groups(UUID(user["sub"]))


@router.patch("/{group_id}", response_model=GroupResponse)
@require_role("admin", "superuser")
async def update_group(
    group_id: UUID,
    body: GroupUpdate,
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    group = await service.edit_group(
        group_id,
        body.name,
        body.bio,
    )

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )

    return group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_role("superuser")
async def delete_group(
    group_id: UUID,
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    await service.delete_group(group_id)


# -------------------------------------------------------------------
# Members
# -------------------------------------------------------------------


@router.post("/{group_id}/members/{user_id}")
@require_role("moderator", "admin", "superuser")
async def add_member(
    group_id: UUID,
    user_id: UUID,
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    await service.add_member(group_id, user_id)

    return {"status": "added"}


@router.delete("/{group_id}/members/{user_id}")
@require_role("moderator", "admin", "superuser")
async def remove_member(
    group_id: UUID,
    user_id: UUID,
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    await service.remove_member(group_id, user_id)

    return {"status": "removed"}


@router.patch("/{group_id}/members/{user_id}/role")
@require_role("moderator", "admin", "superuser")
async def update_member_role(
    group_id: UUID,
    user_id: UUID,
    body: GroupMemberUpdate,
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    await service.update_member_role(
        group_id,
        user_id,
        body.role,
    )

    return {"status": "updated"}


@router.get("/{group_id}/members", response_model=list[GroupMemberResponse])
@require_role("moderator", "admin", "superuser")
async def list_members(
    group_id: UUID,
    user=Depends(inject_user),
    service: GroupService = Depends(_get_service),
):
    return await service.list_members(group_id)

