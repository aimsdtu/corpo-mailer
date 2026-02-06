from fastapi import APIRouter, Depends
from app.api.services.userservice import UserService, get_user_service
from app.api.models.user import User, UserCreate

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(user_in)
