from fastapi import APIRouter, Depends
from app.api.services.groupservice import GroupService, get_group_service
from app.api.models.group import Group, GroupCreate

router = APIRouter()

@router.post("/", response_model=Group)
async def create_group(
    group_in: GroupCreate,
    service: GroupService = Depends(get_group_service)
):
    return await service.create_group(group_in)
