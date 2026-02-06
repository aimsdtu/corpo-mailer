from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class MailStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"

class Mail(BaseModel):
    id: UUID
    subject: str
    body: str
    recipient_group_id: UUID
    sender_id: UUID
    status: MailStatus
    created_at: datetime

class MailCreate(BaseModel):
    subject: str
    body: str
    recipient_group_id: UUID
