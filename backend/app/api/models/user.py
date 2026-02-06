from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class User(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None
    is_active: bool
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None
    password: str
