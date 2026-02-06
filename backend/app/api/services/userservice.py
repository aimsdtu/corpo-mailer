from app.db.protocol import Database
from app.api.models.user import UserCreate, User
from fastapi import Depends
from app.db.session import get_db_session

class UserService:
    def __init__(self, db: Database):
        self.db = db

    async def create_user(self, userInput: UserCreate) -> User:
        raise NotImplementedError

def get_user_service(db: Database = Depends(get_db_session)) -> UserService:
    return UserService(db)


