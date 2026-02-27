from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from enum import Enum


class MailStatus(str, Enum):
    """Mail status enumeration."""
    DRAFT = "draft"
    SENT = "sent"
    FAILED = "failed"


# ---------- Requests ----------

class MailCreate(BaseModel):
    """Request model for creating a mail."""
    subject: str = Field(..., min_length=1, max_length=255, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body content")
    group_id: UUID = Field(..., description="ID of recipient group")
    template_id: UUID | None = Field(None, description="Optional template ID")


class MailUpdate(BaseModel):
    """Request model for updating mail status."""
    status: MailStatus = Field(..., description="Mail status (draft/sent/failed)")


# ---------- Responses ----------

class MailResponse(BaseModel):
    """Response model for mail data."""
    uuid: UUID
    subject: str
    body: str
    group_id: UUID
    created_by: UUID
    template_id: UUID | None
    status: MailStatus
    created_at: datetime
    sent_at: datetime | None = None


class Mail(MailResponse):
    """Alias for compatibility."""
    pass
