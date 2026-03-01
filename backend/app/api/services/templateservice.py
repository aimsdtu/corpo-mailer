"""Template service — CRUD with group-based permission checks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, insert, select, update

from app.api.models.template import TemplateCreate, TemplateUpdate, TemplateResponse
from app.db.database import Database
from app.db.tables import templates, group_members


class TemplateService:
    """Template CRUD operations with group-based access control."""

    def __init__(self, db: Database) -> None:
        self.db = db

    # ── Helpers ────────────────────────────────────────────────────────────

    async def _get_user_group_role(
        self, group_id: UUID, user_id: UUID
    ) -> str | None:
        """Get user's role in a group (user/moderator/admin)."""
        stmt = select(group_members.c.role).where(
            (group_members.c.group_id == group_id)
            & (group_members.c.user_id == user_id)
        )
        row = await self.db.fetch_one(stmt)
        return row["role"] if row else None

    async def _is_moderator_plus(self, group_id: UUID, user_id: UUID) -> bool:
        """Check if user is moderator or higher in group."""
        role = await self._get_user_group_role(group_id, user_id)
        return role in ("moderator", "admin")

    # ── Create ────────────────────────────────────────────────────────────

    async def create_template(
        self, name: str, content: str, created_by: UUID, group_id: UUID
    ) -> TemplateResponse:
        """Create a new template (moderator+ in group only)."""
        if not await self._is_moderator_plus(group_id, created_by):
            raise PermissionError(
                "Only moderators and above can create group templates"
            )

        stmt = (
            insert(templates)
            .values(
                uuid=uuid4(),
                name=name,
                content=content,
                group_id=group_id,
                created_by=created_by,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            .returning(templates)
        )
        row = await self.db.fetch_one(stmt)
        response = TemplateResponse(**row)
        response.can_edit = True  # Creator can always edit
        return response

    # ── Read ───────────────────────────────────────────────────────────────

    async def get_template(
        self, template_id: UUID, user_id: UUID | None = None
    ) -> TemplateResponse | None:
        """Get template by ID with permission check."""
        stmt = select(templates).where(templates.c.uuid == template_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        # Group-scoped template: user must be in that group
        if not row["group_id"]:
            raise PermissionError("Template group scope missing")

        if not user_id:
            raise PermissionError("Must be authenticated to access group templates")

        group_role = await self._get_user_group_role(row["group_id"], user_id)
        if not group_role:
            raise PermissionError(
                "You are not a member of this template's group"
            )

        response = TemplateResponse(**row)
        response.can_edit = await self._is_moderator_plus(
            row["group_id"], user_id
        )

        return response

    async def list_templates(
        self,
        created_by: UUID | None = None,
        group_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> list[TemplateResponse]:
        """List templates with optional filtering."""
        stmt = select(templates)

        if created_by:
            stmt = stmt.where(templates.c.created_by == created_by)

        if group_id:
            if not user_id:
                raise PermissionError("Authentication required")

            if not await self._get_user_group_role(group_id, user_id):
                raise PermissionError("You are not a member of this group")

            stmt = stmt.where(templates.c.group_id == group_id)
        else:
            if user_id:
                stmt = (
                    stmt.join(
                        group_members,
                        templates.c.group_id == group_members.c.group_id,
                    )
                    .where(group_members.c.user_id == user_id)
                )

        stmt = stmt.order_by(templates.c.created_at.desc())
        rows = await self.db.fetch_all(stmt)

        results = []
        for row in rows:
            response = TemplateResponse(**row)
            
            # Set can_edit based on user's role in template group
            if row["group_id"] and user_id:
                response.can_edit = await self._is_moderator_plus(
                    row["group_id"], user_id
                )
            
            results.append(response)

        return results

    # ── Update ─────────────────────────────────────────────────────────────

    async def update_template(
        self, template_id: UUID, user_id: UUID, updates: TemplateUpdate
    ) -> TemplateResponse | None:
        """Update template (moderator+ if group-scoped, owner if global)."""
        # Get template
        stmt = select(templates).where(templates.c.uuid == template_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return None

        # Permission check
        if not row["group_id"]:
            raise PermissionError("Template group scope missing")

        if not await self._is_moderator_plus(row["group_id"], user_id):
            raise PermissionError(
                "Only moderators and above can edit group templates"
            )

        # Build update fields
        fields: dict[str, Any] = {}
        if updates.name is not None:
            fields["name"] = updates.name
        if updates.content is not None:
            fields["content"] = updates.content

        if not fields:
            result = TemplateResponse(**row)
            result.can_edit = True
            return result

        fields["updated_at"] = datetime.now(timezone.utc)

        stmt = (
            update(templates)
            .where(templates.c.uuid == template_id)
            .values(**fields)
            .returning(templates)
        )
        updated_row = await self.db.fetch_one(stmt)
        response = TemplateResponse(**updated_row) if updated_row else None
        if response:
            response.can_edit = True
        return response

    # ── Delete ─────────────────────────────────────────────────────────────

    async def delete_template(self, template_id: UUID, user_id: UUID) -> bool:
        """Delete template (moderator+ if group-scoped, creator if global)."""
        # Get template
        stmt = select(templates).where(templates.c.uuid == template_id)
        row = await self.db.fetch_one(stmt)

        if not row:
            return False

        # Permission check
        if not row["group_id"]:
            raise PermissionError("Template group scope missing")

        if not await self._is_moderator_plus(row["group_id"], user_id):
            raise PermissionError(
                "Only moderators and above can delete group templates"
            )

        stmt = delete(templates).where(templates.c.uuid == template_id)
        await self.db.execute(stmt)
        return True
