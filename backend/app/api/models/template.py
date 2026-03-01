from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


# ---------- Requests ----------

class TemplateCreate(BaseModel):
    """Request model for creating a template."""
    name: str = Field(..., min_length=1, max_length=255, description="Template name")
    content: str = Field(..., min_length=1, description="Template HTML/text content")
    group_id: UUID = Field(..., description="Group UUID")


class TemplateUpdate(BaseModel):
    """Request model for updating a template."""
    name: str | None = Field(None, min_length=1, max_length=255, description="Template name")
    content: str | None = Field(None, min_length=1, description="Template HTML/text content")


# ---------- Responses ----------

class TemplateResponse(BaseModel):
    """Response model for template data."""
    uuid: UUID
    name: str
    content: str
    group_id: UUID | None
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    can_edit: bool = False  # Computed in route based on user role in group


class Template(TemplateResponse):
    """Alias for compatibility."""
    pass
