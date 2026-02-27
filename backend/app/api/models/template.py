from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


# ---------- Requests ----------

class TemplateCreate(BaseModel):
    """Request model for creating a template."""
    name: str = Field(..., min_length=1, max_length=255, description="Template name")
    content: str = Field(..., min_length=1, description="Template HTML/text content")


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
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class Template(TemplateResponse):
    """Alias for compatibility."""
    pass
