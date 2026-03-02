from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from enum import Enum


class MailStatus(str, Enum):
    """Mail status enumeration with approval workflow."""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SENT = "sent"
    FAILED = "failed"


# ---------- Mail Diff Models ----------

class MailDiffResponse(BaseModel):
    """Response model for mail edit history."""
    id: str
    mail_id: UUID
    field_name: str  # subject | body
    old_value: str | None
    new_value: str
    edited_by: UUID
    editor_role: str  # user | moderator | admin | owner
    edited_at: datetime


# ---------- Requests ----------

class MailCreate(BaseModel):
    """Request model for creating a mail draft."""
    subject: str = Field(..., min_length=1, max_length=255, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body content (user-editable)")
    llm_body: str | None = Field(None, description="Optional: AI-generated body (stored separately)")
    group_id: UUID = Field(..., description="ID of recipient group")
    template_id: UUID = Field(..., description="Template ID")


class MailUpdate(BaseModel):
    """Request model for updating mail (edits to body/subject)."""
    subject: str | None = Field(None, min_length=1, max_length=255, description="Updated subject")
    body: str | None = Field(None, min_length=1, description="Updated body")


class MailApprovalRequest(BaseModel):
    """Request model for approving/rejecting mail."""
    approved: bool = Field(..., description="True to approve, False to reject")


# ---------- Responses ----------

class MailResponse(BaseModel):
    """Response model for mail data with full context."""
    uuid: UUID
    subject: str
    body: str
    llm_body: str | None  # AI-generated body (separate)
    group_id: UUID
    created_by: UUID
    template_id: UUID | None
    status: MailStatus
    approved_by: UUID | None  # Who approved (mod/admin/owner)
    approved_at: datetime | None  # When approved
    diffs: list[MailDiffResponse] = []  # Edit history
    created_at: datetime
    sent_at: datetime | None = None


class Mail(MailResponse):
    """Alias for compatibility."""
    pass
