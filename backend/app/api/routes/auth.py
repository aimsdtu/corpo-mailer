from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.services.authservice import AuthService, get_auth_service
from app.api.models.auth import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
):
    return await service.authenticate_user(form_data.username, form_data.password)
