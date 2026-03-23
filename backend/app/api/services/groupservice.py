from app.db.database import Database
from app.api.models.group import GroupCreate, Group
from app.api.models.auth import Token
from fastapi import Depends
from app.db.session import get_db

class GroupService:
    def __init__(self, db: Database):
        self.db = db

    async def create_group(self, groupIn: GroupCreate, ownerDetails = Token) -> Group:
        raise NotImplementedError

def get_group_service(db: Database = Depends(get_db)) -> GroupService:
    return GroupService(db)
