import code
import hashlib
import uuid
import random
from datetime import datetime, timedelta

from const.const import *
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from email.mime.text import MIMEText

from database import get_db

from models.user import User
from models.verification_models import VerificationCode
from schemas.user_schema import UserCreate, UserResponse, UserRegistrationResponse
from controller.user_controller import register_user_controller

router = APIRouter()



@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        id=uuid.uuid4(),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=user.password,  # will hash later
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/register", response_model=UserRegistrationResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register_user_controller(user, db)


def generate_otp():
    return str(random.randint(100000, 999999))

def generate_verification_code(user_id: uuid.UUID, db: Session, verification_type: str):
    code = generate_otp()
    expiration = datetime.utcnow() + timedelta(minutes=1)  # OTP valid for 1 minutes
    
    verification_token = VerificationCode(
        token=code,   # storing 6-digit code
        expiration=expiration,
        user_id=user_id,
        type=verification_type
    )
    
    db.add(verification_token)
    db.commit()
    
    return code





@router.post("/verify")
def verify_code(user_id: uuid.UUID, code: str, db: Session = Depends(get_db)):
    
    verification = db.query(VerificationToken).filter(
        VerificationToken.user_id == user_id,
        VerificationToken.token == code
    ).first()

    if verification is None:
        raise create_error(400, detail="Invalid verification code")
    if verification.expiration < datetime.utcnow():
        raise create_error(400, detail="Verification code expired")

    user = db.query(UserInDB).filter(UserInDB.id == user_id).first()

    user.is_verified = True
    db.commit()

    db.delete(verification)
    db.commit()

    return {"message": "User verified successfully"}

# hashed_code = hashlib.sha256(code.encode()).hexdigest()
@router.post("/resend-verification")
def resend_verification(user_id: uuid.UUID, verification_type: str, db: Session = Depends(get_db)):
    user = db.query(UserInDB).filter(UserInDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    verification = db.query(VerificationToken).filter(
        VerificationToken.user_id == user_id, VerificationToken.type == verification_type
    ).first()

    if verification:
        db.delete(verification)
        db.commit()

    token = generate_verification_token(user_id, db, verification_type)

    if verification_type == "email":
        send_verification_email(user.email, token)
    elif verification_type == "sms":
        send_verification_sms(user.phone_number, token)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification type")

    return {"message": "Verification token resent"}