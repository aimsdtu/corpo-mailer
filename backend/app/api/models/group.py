from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Group(BaseModel):
    id: UUID
    name: str
    description: str | None
    owner_id: UUID
    created_at: datetime

class GroupCreate(BaseModel):
    name: str
    description: str | None
