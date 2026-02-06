from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Template(BaseModel):
    id: UUID
    name: str
    content: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

class TemplateCreate(BaseModel):
    name: str
    content: str
