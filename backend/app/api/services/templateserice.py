from app.db.database import Database
from app.api.models.template import TemplateCreate, Template
from app.api.models.auth import Token
from fastapi import Depends
from app.db.session import get_db

class TemplateService:
    def __init__(self, db: Database):
        self.db = db

    async def create_template(self, templateIn: TemplateCreate, ownerDetails = Token) -> Template:
        raise NotImplementedError

def get_template_service(db: Database = Depends(get_db)) -> TemplateService:
    return TemplateService(db)
