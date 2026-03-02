"""Mail service — CRUD with group-scoped permissions, approvals, and diff tracking."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, insert, select, update

from app.api.models.mail import MailCreate, MailUpdate, MailResponse, MailStatus, MailDiffResponse
from app.db.database import Database
from app.db.tables import mails, groups, group_members, mail_diffs, templates


class MailService:
    """Mail CRUD operations with group-based access control and approval workflow."""

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

    async def _get_group_role(self, group_id: UUID, user_id: UUID) -> str | None:
        """Get user's role in group."""
        stmt = select(group_members.c.role).where(
            (group_members.c.group_id == group_id)
            & (group_members.c.user_id == user_id)
        )
        row = await self.db.fetch_one(stmt)
        return row["role"] if row else None

    async def _is_mod_plus(self, group_id: UUID, user_id: UUID) -> bool:
        """Check if user is moderator or admin in group."""
        role = await self._get_group_role(group_id, user_id)
        return role in ("moderator", "admin")

    async def _get_mail_diffs(self, mail_id: UUID) -> list[MailDiffResponse]:
        """Get edit history for a mail."""
        stmt = (
            select(mail_diffs)
            .where(mail_diffs.c.mail_id == mail_id)
            .order_by(mail_diffs.c.edited_at.desc())
        )
        rows = await self.db.fetch_all(stmt)
        return [MailDiffResponse(**row) for row in rows]

    async def _to_response(self, row: dict) -> MailResponse:
        """Convert DB row to MailResponse with diffs."""
        diffs = await self._get_mail_diffs(row["uuid"])
        payload = dict(row)
        payload["diffs"] = diffs
        return MailResponse(**payload)

    async def _group_exists(self, group_id: UUID) -> bool:
        """Check if group exists."""
        stmt = select(groups).where(groups.c.uuid == group_id)
        return await self.db.fetch_one(stmt) is not None

    async def _validate_template_scope(
        self,
        template_id: UUID,
        group_id: UUID,
        user_id: UUID,
    ) -> None:
        """Ensure template belongs to the same group and user can access it."""
        stmt = select(templates).where(templates.c.uuid == template_id)
        row = await self.db.fetch_one(stmt)
        if not row:
            raise ValueError("Template not found")

        if row["group_id"] != group_id:
            raise PermissionError("Template is not scoped to this group")

        if not await self._verify_group_access(group_id, user_id):
            raise PermissionError("You are not a member of this template's group")

    # ── Create ────────────────────────────────────────────────────────────

    async def create_mail(
        self,
        subject: str,
        body: str,
        llm_body: str | None,
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

        if template_id is not None:
            await self._validate_template_scope(template_id, group_id, created_by)

        stmt = (
            insert(mails)
            .values(
                uuid=uuid4(),
                subject=subject,
                body=body,
                llm_body=llm_body,
                group_id=group_id,
                template_id=template_id,
                created_by=created_by,
                status=MailStatus.DRAFT.value,
                created_at=datetime.now(timezone.utc),
            )
            .returning(mails)
        )
        row = await self.db.fetch_one(stmt)
        return await self._to_response(row)

    # ── Read ───────────────────────────────────────────────────────────────

    async def get_mail(self, mail_id: UUID, user_id: UUID) -> MailResponse | None:
        """Get mail (owner or mod+ in group)."""
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        # Owner can view, otherwise require mod+
        if row["created_by"] != user_id:
            if not await self._is_mod_plus(row["group_id"], user_id):
                raise PermissionError("You can only view your own mails unless you're moderator+")

        return await self._to_response(row)

    async def list_mails(self, created_by: UUID) -> list[MailResponse]:
        """List mails created by user."""
        stmt = (
            select(mails)
            .where(mails.c.created_by == created_by)
            .order_by(mails.c.created_at.desc())
        )
        rows = await self.db.fetch_all(stmt)
        return [await self._to_response(row) for row in rows]

    async def list_group_mails(self, group_id: UUID, user_id: UUID) -> list[MailResponse]:
        """List mails for a group.

        - mod+ sees all group mails
        - members see only their own
        """
        if not await self._verify_group_access(group_id, user_id):
            raise PermissionError("You are not a member of this group")

        stmt = select(mails).where(mails.c.group_id == group_id)
        if not await self._is_mod_plus(group_id, user_id):
            stmt = stmt.where(mails.c.created_by == user_id)

        stmt = stmt.order_by(mails.c.created_at.desc())
        rows = await self.db.fetch_all(stmt)
        return [await self._to_response(row) for row in rows]

    # ── Update ─────────────────────────────────────────────────────────────

    async def update_mail(
        self, mail_id: UUID, user_id: UUID, updates: MailUpdate
    ) -> MailResponse | None:
        """Update mail subject/body with diff tracking (draft only)."""
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        # Must be draft for edits
        if row["status"] != MailStatus.DRAFT.value:
            raise ValueError("Can only edit draft mails")

        # Owner or mod+
        is_owner = row["created_by"] == user_id
        is_mod_plus = await self._is_mod_plus(row["group_id"], user_id)
        if not is_owner and not is_mod_plus:
            raise PermissionError("You can only edit your own mails unless you're moderator+")

        editor_role = "owner" if is_owner else (await self._get_group_role(row["group_id"], user_id) or "user")

        fields: dict[str, Any] = {}

        if updates.subject is not None and updates.subject != row["subject"]:
            fields["subject"] = updates.subject
            await self.db.execute(
                insert(mail_diffs).values(
                    id=uuid4(),
                    mail_id=mail_id,
                    field_name="subject",
                    old_value=row["subject"],
                    new_value=updates.subject,
                    edited_by=user_id,
                    editor_role=editor_role,
                    edited_at=datetime.now(timezone.utc),
                )
            )

        if updates.body is not None and updates.body != row["body"]:
            fields["body"] = updates.body
            await self.db.execute(
                insert(mail_diffs).values(
                    id=uuid4(),
                    mail_id=mail_id,
                    field_name="body",
                    old_value=row["body"],
                    new_value=updates.body,
                    edited_by=user_id,
                    editor_role=editor_role,
                    edited_at=datetime.now(timezone.utc),
                )
            )

        if not fields:
            return await self._to_response(row)

        stmt = (
            update(mails)
            .where(mails.c.uuid == mail_id)
            .values(**fields)
            .returning(mails)
        )
        updated_row = await self.db.fetch_one(stmt)
        return await self._to_response(updated_row) if updated_row else None

    async def submit_for_approval(self, mail_id: UUID, user_id: UUID) -> MailResponse | None:
        """Submit draft mail for approval (any group member)."""
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        if not await self._verify_group_access(row["group_id"], user_id):
            raise PermissionError("Only group members can submit for approval")

        if row["status"] != MailStatus.DRAFT.value:
            raise ValueError("Only draft mails can be submitted for approval")

        stmt = (
            update(mails)
            .where(mails.c.uuid == mail_id)
            .values(status=MailStatus.PENDING_APPROVAL.value)
            .returning(mails)
        )
        updated_row = await self.db.fetch_one(stmt)
        return await self._to_response(updated_row) if updated_row else None

    async def approve_mail(self, mail_id: UUID, approver_id: UUID) -> MailResponse | None:
        """Approve mail (moderator/admin/owner in group)."""
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        # Must be pending approval
        if row["status"] != MailStatus.PENDING_APPROVAL.value:
            raise ValueError("Only pending mails can be approved")

        is_owner = row["created_by"] == approver_id
        is_mod_plus = await self._is_mod_plus(row["group_id"], approver_id)
        if not is_owner and not is_mod_plus:
            raise PermissionError("Only owner or moderator+ can approve")

        stmt = (
            update(mails)
            .where(mails.c.uuid == mail_id)
            .values(
                status=MailStatus.APPROVED.value,
                approved_by=approver_id,
                approved_at=datetime.now(timezone.utc),
            )
            .returning(mails)
        )
        updated_row = await self.db.fetch_one(stmt)
        return await self._to_response(updated_row) if updated_row else None

    async def reject_mail(self, mail_id: UUID, approver_id: UUID) -> MailResponse | None:
        """Reject mail (moderator/admin/owner in group) - returns to draft."""
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        # Must be pending approval
        if row["status"] != MailStatus.PENDING_APPROVAL.value:
            raise ValueError("Only pending mails can be rejected")

        is_owner = row["created_by"] == approver_id
        is_mod_plus = await self._is_mod_plus(row["group_id"], approver_id)
        if not is_owner and not is_mod_plus:
            raise PermissionError("Only owner or moderator+ can reject")

        stmt = (
            update(mails)
            .where(mails.c.uuid == mail_id)
            .values(
                status=MailStatus.DRAFT.value,
                approved_by=approver_id,
                approved_at=datetime.now(timezone.utc),
            )
            .returning(mails)
        )
        updated_row = await self.db.fetch_one(stmt)
        return await self._to_response(updated_row) if updated_row else None

    async def mark_sent(self, mail_id: UUID, user_id: UUID) -> MailResponse | None:
        """Mark approved mail as sent (owner or mod+)."""
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        if row["status"] != MailStatus.APPROVED.value:
            raise ValueError("Only approved mails can be sent")

        is_owner = row["created_by"] == user_id
        is_mod_plus = await self._is_mod_plus(row["group_id"], user_id)
        if not is_owner and not is_mod_plus:
            raise PermissionError("Only owner or moderator+ can send")

        stmt = (
            update(mails)
            .where(mails.c.uuid == mail_id)
            .values(
                status=MailStatus.SENT.value,
                sent_at=datetime.now(timezone.utc),
            )
            .returning(mails)
        )
        updated_row = await self.db.fetch_one(stmt)
        return await self._to_response(updated_row) if updated_row else None

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

    async def get_mail_diffs(self, mail_id: UUID, user_id: UUID) -> list[MailDiffResponse]:
        """Get mail edit history (owner or mod+)."""
        stmt = select(mails).where(mails.c.uuid == mail_id)
        row = await self.db.fetch_one(stmt)
        if not row:
            raise ValueError("Mail not found")

        is_owner = row["created_by"] == user_id
        is_mod_plus = await self._is_mod_plus(row["group_id"], user_id)
        if not is_owner and not is_mod_plus:
            raise PermissionError("You cannot view edit history for this mail")

        return await self._get_mail_diffs(mail_id)
