from app.db.database import Database
from app.api.models.mail import MailCreate, Mail
from fastapi import Depends
from app.db.session import get_db

class MailService:
    def __init__(self, db: Database):
        self.db = db

    async def send_mail(self, mail_in: MailCreate, sender_id: int) -> Mail:
        raise NotImplementedError

def get_mail_service(db: Database = Depends(get_db)) -> MailService:
    return MailService(db)
