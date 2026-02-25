from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from const.const import create_error, get_password_hash
from controller.user_controller import (
    generate_verification_code,
    register_user_controller,
    send_verification_email,
    send_verification_sms,
)
from database import get_db
from models.user import User
from models.verification_models import VerificationCode
from schemas.user_schema import UserCreate, UserRegistrationResponse, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise create_error(400, "Email already registered")

    db_user = User(
        email=user.email,
        password_hash=get_password_hash(user.password),
        phone=user.phone_number if user.phone_number else None,
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


@router.post("/verify")
def verify_code(
    user_id: int,
    code: str,
    verification_type: str = "email",
    db: Session = Depends(get_db),
):
    verification = db.query(VerificationCode).filter(
        VerificationCode.user_id == user_id,
        VerificationCode.token == code,
        VerificationCode.type == verification_type,
    ).first()

    if verification is None:
        raise create_error(400, "Invalid verification code")

    if verification.expiration < datetime.utcnow():
        db.delete(verification)
        db.commit()
        raise create_error(400, "Verification code expired")

    db.delete(verification)
    db.commit()
    return {"message": f"{verification_type} verified successfully"}


@router.post("/resend-verification")
def resend_verification(
    user_id: int,
    verification_type: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise create_error(404, "User not found")

    db.query(VerificationCode).filter(
        VerificationCode.user_id == user_id,
        VerificationCode.type == verification_type,
    ).delete()
    db.commit()

    code = generate_verification_code(user_id, db, verification_type)

    if verification_type == "email":
        send_verification_email(user.email, code)
    elif verification_type == "sms":
        if not user.phone:
            raise create_error(400, "User does not have a phone number")
        send_verification_sms(user.phone, code)
    else:
        raise create_error(400, "Invalid verification type")

    return {"message": "Verification code resent"}
