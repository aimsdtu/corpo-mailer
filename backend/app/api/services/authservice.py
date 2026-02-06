from app.db.protocol import Database
from app.api.models.auth import Token
from datetime import timedelta
from typing import Any
from fastapi import Depends
from app.db.session import get_db_session

class AuthService:
    def __init__(self, db: Database):
        self.db = db

    async def authenticate_user(self, email: str, password: str) -> Any:
        raise NotImplementedError

    async def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> Token:
        raise NotImplementedError

def get_auth_service(db: Database = Depends(get_db_session)) -> AuthService:
    return AuthService(db)
