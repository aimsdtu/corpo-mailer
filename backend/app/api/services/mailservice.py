"""Mail service — CRUD with group access and permission checks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, insert, select, update

from app.api.models.mail import MailCreate, MailUpdate, MailResponse, MailStatus
from app.db.database import Database
from app.db.tables import mails, groups, group_members


class MailService:
    """Mail CRUD operations with group-based access control."""

    def __init__(self, db: Database) -> None:
        self.db = db

    # ── Helpers ────────────────────────────────────────────────────────────

    async def _verify_group_access(self, group_id: UUID, user_id: UUID) -> bool:
        """Check if user is a member of the group."""
        stmt = select(group_members).where(
            (group_members.c.group_id == group_id)
            & (group_members.c.user_id == user_id)
        )
        return await self.db.fetch_one(stmt) is not None

    async def _group_exists(self, group_id: UUID) -> bool:
        """Check if group exists."""
        stmt = select(groups).where(groups.c.uuid == group_id)
        return await self.db.fetch_one(stmt) is not None

    # ── Create ────────────────────────────────────────────────────────────

    async def create_mail(
        self,
        subject: str,
        body: str,
        group_id: UUID,
        created_by: UUID,
        template_id: UUID | None = None,
    ) -> MailResponse:
        """Create a new mail draft."""
        # Verify group exists and user is a member
        if not await self._group_exists(group_id):
            raise ValueError("Group not found")

        if not await self._verify_group_access(group_id, created_by):
            raise PermissionError("You are not a member of this group")

        stmt = (
            insert(mails)
            .values(
                uuid=uuid4(),
                subject=subject,
                body=body,
                group_id=group_id,
                template_id=template_id,
                created_by=created_by,
                status=MailStatus.DRAFT.value,
                created_at=datetime.now(timezone.utc),
            )
            .returning(mails)
        )
        row = await self.db.fetch_one(stmt)
        return MailResponse(**row)

    # ── Read ───────────────────────────────────────────────────────────────

    async def get_mail(self, mail_id: UUID, user_id: UUID) -> MailResponse | None:
        """Get mail (owner or admin only)."""
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        # Check ownership
        if row["created_by"] != user_id:
            raise PermissionError("You can only view your own mails")

        return MailResponse(**row)

    async def list_mails(self, created_by: UUID) -> list[MailResponse]:
        """List mails created by user."""
        stmt = (
            select(mails)
            .where(mails.c.created_by == created_by)
            .order_by(mails.c.created_at.desc())
        )
        rows = await self.db.fetch_all(stmt)
        return [MailResponse(**row) for row in rows]

    async def list_group_mails(self, group_id: UUID) -> list[MailResponse]:
        """List all mails for a group."""
        stmt = (
            select(mails)
            .where(mails.c.group_id == group_id)
            .order_by(mails.c.created_at.desc())
        )
        rows = await self.db.fetch_all(stmt)
        return [MailResponse(**row) for row in rows]

    # ── Update ─────────────────────────────────────────────────────────────

    async def update_mail_status(
        self, mail_id: UUID, user_id: UUID, status: MailStatus
    ) -> MailResponse | None:
        """Update mail status (owner only)."""
        # Get mail and check ownership
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        if row["created_by"] != user_id:
            raise PermissionError("You can only update your own mails")

        # Build update
        fields: dict[str, Any] = {"status": status.value}

        if status == MailStatus.SENT:
            fields["sent_at"] = datetime.now(timezone.utc)

        stmt = (
            update(mails)
            .where(mails.c.uuid == mail_id)
            .values(**fields)
            .returning(mails)
        )
        updated_row = await self.db.fetch_one(stmt)
        return MailResponse(**updated_row) if updated_row else None

    # ── Delete ─────────────────────────────────────────────────────────────

    async def delete_mail(self, mail_id: UUID, user_id: UUID) -> bool:
        """Delete mail (owner only, must be draft)."""
        # Get mail
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return False

        # Check ownership
        if row["created_by"] != user_id:
            raise PermissionError("You can only delete your own mails")

        # Only allow deleting drafts
        if row["status"] != MailStatus.DRAFT.value:
            raise ValueError("Can only delete draft mails")

        stmt = delete(mails).where(mails.c.uuid == mail_id)
        await self.db.execute(stmt)
        return True
