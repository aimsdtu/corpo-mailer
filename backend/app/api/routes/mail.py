"""Mail routes — CRUD with group access, approval, and diff tracking."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.auth import inject_user, require_role
from app.api.models.mail import (
    MailCreate,
    MailDiffResponse,
    MailUpdate,
    MailResponse,
)
from app.api.services.mailservice import MailService
from app.db.database import Database
from app.db.session import get_db


router = APIRouter(prefix="/mails", tags=["mails"])


def _get_service(db: Database = Depends(get_db)) -> MailService:
    return MailService(db)


@router.post("", response_model=MailResponse, status_code=status.HTTP_201_CREATED)
@require_role("user", "admin", "moderator", "superuser")
async def create_mail(
    body: MailCreate,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Create a new mail draft."""
    try:
        return await service.create_mail(
            subject=body.subject,
            body=body.body,
            llm_body=body.llm_body,
            group_id=body.group_id,
            created_by=UUID(user["sub"]),
            template_id=body.template_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/{mail_id}", response_model=MailResponse)
@require_role("user", "admin", "moderator", "superuser")
async def get_mail(
    mail_id: UUID,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Get mail by ID (owner only)."""
    try:
        mail = await service.get_mail(mail_id=mail_id, user_id=UUID(user["sub"]))
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    if not mail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mail not found",
        )
    return mail


@router.get("", response_model=list[MailResponse])
@require_role("user", "admin", "moderator", "superuser")
async def list_mails(
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """List user's mails."""
    return await service.list_mails(created_by=UUID(user["sub"]))


@router.get("/groups/{group_id}", response_model=list[MailResponse])
@require_role("user", "admin", "moderator", "superuser")
async def list_group_mails(
    group_id: UUID,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """List mails for a group.

    - members: only own mails
    - moderator+: all group mails
    """
    try:
        return await service.list_group_mails(group_id=group_id, user_id=UUID(user["sub"]))
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.patch("/{mail_id}", response_model=MailResponse)
@require_role("user", "admin", "moderator", "superuser")
async def update_mail(
    mail_id: UUID,
    body: MailUpdate,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Update mail subject/body (draft only, owner or mod+)."""
    try:
        mail = await service.update_mail(
            mail_id=mail_id,
            user_id=UUID(user["sub"]),
            updates=body,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if not mail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mail not found",
        )
    return mail


@router.post("/{mail_id}/submit", response_model=MailResponse)
@require_role("user", "admin", "moderator", "superuser")
async def submit_mail(
    mail_id: UUID,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Submit draft for approval (any group member)."""
    try:
        mail = await service.submit_for_approval(
            mail_id=mail_id,
            user_id=UUID(user["sub"]),
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    return mail


@router.post("/{mail_id}/approve", response_model=MailResponse)
@require_role("user", "admin", "moderator", "superuser")
async def approve_mail(
    mail_id: UUID,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Approve pending mail (owner or moderator+)."""
    try:
        mail = await service.approve_mail(
            mail_id=mail_id,
            approver_id=UUID(user["sub"]),
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    return mail


@router.post("/{mail_id}/reject", response_model=MailResponse)
@require_role("user", "admin", "moderator", "superuser")
async def reject_mail(
    mail_id: UUID,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Reject pending mail (owner or moderator+), returns to draft."""
    try:
        mail = await service.reject_mail(
            mail_id=mail_id,
            approver_id=UUID(user["sub"]),
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    return mail


@router.post("/{mail_id}/send", response_model=MailResponse)
@require_role("user", "admin", "moderator", "superuser")
async def send_mail(
    mail_id: UUID,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Mark approved mail as sent (owner or mod+)."""
    try:
        mail = await service.mark_sent(
            mail_id=mail_id,
            user_id=UUID(user["sub"]),
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mail not found")
    return mail


@router.get("/{mail_id}/diffs", response_model=list[MailDiffResponse])
@require_role("user", "admin", "moderator", "superuser")
async def get_mail_diffs(
    mail_id: UUID,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Get mail edit history (owner or mod+)."""
    try:
        return await service.get_mail_diffs(
            mail_id=mail_id,
            user_id=UUID(user["sub"]),
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{mail_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_role("user", "admin", "moderator", "superuser")
async def delete_mail(
    mail_id: UUID,
    user=Depends(inject_user),
    service: MailService = Depends(_get_service),
):
    """Delete mail (owner only, must be draft)."""
    try:
        deleted = await service.delete_mail(
            mail_id=mail_id,
            user_id=UUID(user["sub"]),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mail not found",
        )
