from fastapi import APIRouter, Depends
from app.api.services.mailservice import MailService, get_mail_service
from app.api.models.mail import Mail, MailCreate

router = APIRouter()

@router.post("/", response_model=Mail)
async def send_mail(
    mail_in: MailCreate,
    service: MailService = Depends(get_mail_service)
):
    # sender_id should ideally come from auth, but using a placeholder for now
    return await service.send_mail(mail_in, sender_id=0)
