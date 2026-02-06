from fastapi import APIRouter, Depends
from app.api.services.templateserice import TemplateService, get_template_service
from app.api.models.template import Template, TemplateCreate

router = APIRouter()

@router.post("/", response_model=Template)
async def create_template(
    template_in: TemplateCreate,
    service: TemplateService = Depends(get_template_service)
):
    return await service.create_template(template_in)
