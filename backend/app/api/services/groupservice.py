from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlalchemy import insert, select, update, delete

from app.db.database import Database
from app.db.tables import groups, group_members


class GroupService:

    def __init__(self, db: Database):
        self.db = db

    # ---------------- Groups ----------------

    async def create_group(self, name: str, bio: str, owner_id: UUID):

        stmt = (
            insert(groups)
            .values(
                uuid=uuid4(),
                name=name,
                bio=bio,
                created_by=owner_id,
                created_at=datetime.now(timezone.utc),
            )
            .returning(groups)
        )

        group = await self.db.fetch_one(stmt)

        # creator becomes admin
        await self.add_member(group["uuid"], owner_id, "admin")

        return group

    async def edit_group(self, group_id: UUID, name: str | None, bio: str | None):

        fields = {}

        if name is not None:
            fields["name"] = name

        if bio is not None:
            fields["bio"] = bio

        if not fields:
            return await self.get_group(group_id)

        stmt = (
            update(groups)
            .where(groups.c.uuid == group_id)
            .values(**fields)
            .returning(groups)
        )

        return await self.db.fetch_one(stmt)

    async def get_group(self, group_id: UUID):

        stmt = select(groups).where(groups.c.uuid == group_id)

        return await self.db.fetch_one(stmt)

    async def list_groups(self):

        stmt = select(groups).order_by(groups.c.created_at.desc())

        return await self.db.fetch_all(stmt)

    async def delete_group(self, group_id: UUID):

        await self.db.execute(
            delete(group_members).where(
                group_members.c.group_id == group_id
            )
        )

        await self.db.execute(
            delete(groups).where(groups.c.uuid == group_id)
        )

    # ---------------- Members ----------------

    async def add_member(
        self,
        group_id: UUID,
        user_id: UUID,
        role: str = "user",
    ):

        stmt = insert(group_members).values(
            group_id=group_id,
            user_id=user_id,
            role=role,
            joined_at=datetime.now(timezone.utc),
        )

        await self.db.execute(stmt)

    async def remove_member(self, group_id: UUID, user_id: UUID):

        stmt = delete(group_members).where(
            group_members.c.group_id == group_id,
            group_members.c.user_id == user_id,
        )

        await self.db.execute(stmt)

    async def update_member_role(
        self,
        group_id: UUID,
        user_id: UUID,
        role: str,
    ):

        stmt = (
            update(group_members)
            .where(
                group_members.c.group_id == group_id,
                group_members.c.user_id == user_id,
            )
            .values(role=role)
        )

        await self.db.execute(stmt)

    async def get_member_role(self, group_id: UUID, user_id: UUID):

        stmt = select(group_members.c.role).where(
            group_members.c.group_id == group_id,
            group_members.c.user_id == user_id,
        )

        row = await self.db.fetch_one(stmt)

        return row["role"] if row else None

    async def list_members(self, group_id: UUID):

        stmt = select(group_members).where(
            group_members.c.group_id == group_id
        )

        return await self.db.fetch_all(stmt)

    async def get_user_groups(self, user_id: UUID):

        stmt = (
            select(groups)
            .join(
                group_members,
                groups.c.uuid == group_members.c.group_id,
            )
            .where(group_members.c.user_id == user_id)
        )

        return await self.db.fetch_all(stmt)