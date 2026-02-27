"""Template routes — CRUD with auth and permission checks."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.auth import inject_user, require_role
from app.api.models.template import TemplateCreate, TemplateUpdate, TemplateResponse
from app.api.services.templateservice import TemplateService
from app.db.database import Database
from app.db.session import get_db


router = APIRouter(prefix="/templates", tags=["templates"])


def _get_service(db: Database = Depends(get_db)) -> TemplateService:
    return TemplateService(db)


@router.post("", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
@require_role("user", "admin", "moderator", "superuser")
async def create_template(
    body: TemplateCreate,
    user=Depends(inject_user),
    service: TemplateService = Depends(_get_service),
):
    """Create a new email template."""
    return await service.create_template(
        name=body.name,
        content=body.content,
        created_by=UUID(user["sub"]),
    )


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: UUID,
    service: TemplateService = Depends(_get_service),
):
    """Get template by ID."""
    template = await service.get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )
    return template


@router.get("", response_model=list[TemplateResponse])
async def list_templates(
    user=Depends(inject_user),
    service: TemplateService = Depends(_get_service),
):
    """List user's templates."""
    return await service.list_templates(created_by=UUID(user["sub"]))


@router.patch("/{template_id}", response_model=TemplateResponse)
@require_role("user", "admin", "moderator", "superuser")
async def update_template(
    template_id: UUID,
    body: TemplateUpdate,
    user=Depends(inject_user),
    service: TemplateService = Depends(_get_service),
):
    """Update template (owner only)."""
    try:
        template = await service.update_template(
            template_id=template_id,
            user_id=UUID(user["sub"]),
            updates=body,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )

    return template


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_role("user", "admin", "moderator", "superuser")
async def delete_template(
    template_id: UUID,
    user=Depends(inject_user),
    service: TemplateService = Depends(_get_service),
):
    """Delete template (owner only)."""
    try:
        deleted = await service.delete_template(
            template_id=template_id,
            user_id=UUID(user["sub"]),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found",
        )
