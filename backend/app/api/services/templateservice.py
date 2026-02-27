"""Template service — CRUD with permission checks."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, insert, select, update

from app.api.models.template import TemplateCreate, TemplateUpdate, TemplateResponse
from app.db.database import Database
from app.db.tables import templates


class TemplateService:
    """Template CRUD operations with ownership-based access control."""

    def __init__(self, db: Database) -> None:
        self.db = db

    # ── Create ────────────────────────────────────────────────────────────

    async def create_template(
        self, name: str, content: str, created_by: UUID
    ) -> TemplateResponse:
        """Create a new template."""
        stmt = (
            insert(templates)
            .values(
                uuid=uuid4(),
                name=name,
                content=content,
                created_by=created_by,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            .returning(templates)
        )
        row = await self.db.fetch_one(stmt)
        return TemplateResponse(**row)

    # ── Read ───────────────────────────────────────────────────────────────

    async def get_template(self, template_id: UUID) -> TemplateResponse | None:
        """Get template by ID (no permission check — public read)."""
        stmt = select(templates).where(templates.c.uuid == template_id)
        row = await self.db.fetch_one(stmt)
        return TemplateResponse(**row) if row else None

    async def list_templates(self, created_by: UUID | None = None) -> list[TemplateResponse]:
        """List templates, optionally filtered by creator."""
        stmt = select(templates)
        if created_by:
            stmt = stmt.where(templates.c.created_by == created_by)
        stmt = stmt.order_by(templates.c.created_at.desc())
        rows = await self.db.fetch_all(stmt)
        return [TemplateResponse(**row) for row in rows]

    # ── Update ─────────────────────────────────────────────────────────────

    async def update_template(
        self, template_id: UUID, user_id: UUID, updates: TemplateUpdate
    ) -> TemplateResponse | None:
        """Update template (owner or admin only)."""
        # Check ownership
        template = await self.get_template(template_id)
        if not template:
            return None

        if template.created_by != user_id:
            raise PermissionError("You can only edit your own templates")

        # Build update fields
        fields: dict[str, Any] = {}
        if updates.name is not None:
            fields["name"] = updates.name
        if updates.content is not None:
            fields["content"] = updates.content

        if not fields:
            return template

        fields["updated_at"] = datetime.now(timezone.utc)

        stmt = (
            update(templates)
            .where(templates.c.uuid == template_id)
            .values(**fields)
            .returning(templates)
        )
        row = await self.db.fetch_one(stmt)
        return TemplateResponse(**row) if row else None

    # ── Delete ─────────────────────────────────────────────────────────────

    async def delete_template(self, template_id: UUID, user_id: UUID) -> bool:
        """Delete template (owner or admin only)."""
        # Check ownership
        template = await self.get_template(template_id)
        if not template:
            return False

        if template.created_by != user_id:
            raise PermissionError("You can only delete your own templates")

        stmt = delete(templates).where(templates.c.uuid == template_id)
        await self.db.execute(stmt)
        return True
