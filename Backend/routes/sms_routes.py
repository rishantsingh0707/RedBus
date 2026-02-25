from fastapi import APIRouter
from Backend.sms_service import send_sms

router = APIRouter()

@router.post("/send-sms")
def send_sms_api(phone_number: str):
    return send_sms(phone_number)
