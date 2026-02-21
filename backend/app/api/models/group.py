from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# ---------- Requests ----------

class GroupCreate(BaseModel):
    name: str
    bio: str | None = None


class GroupUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None


class GroupMemberUpdate(BaseModel):
    role: str  # user | moderator | admin


# ---------- Responses ----------

class GroupResponse(BaseModel):
    uuid: UUID
    name: str
    bio: str | None
    created_by: UUID
    created_at: datetime


class GroupMemberResponse(BaseModel):
    user_id: UUID
    role: str
    joined_at: datetime