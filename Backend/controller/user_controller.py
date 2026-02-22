import random
from schemas.user_schema import UserCreate, UserResponse, UserRegistrationResponse
from models.user import User
from models.verification_models import VerificationCode
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from const.const import *
def register_user_controller(user: UserCreate, db: Session):

    # 1️⃣ Check existing email
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise create_error(400, "Email already registered")

    # 2️⃣ Hash password
    hashed_password = get_password_hash(user.password)

    # 3️⃣ Create user
    new_user = User(
        email=user.email,
        password_hash=hashed_password,
        phone=user.phone_number if user.phone_number else None,
        # is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 4️⃣ Generate & send OTP
    email_code = generate_verification_code(new_user.id, db, "email")
    send_verification_email(new_user.email, email_code)

    if user.phone_number:
        sms_code = generate_verification_code(new_user.id, db, "sms")
        send_verification_sms(user.phone_number, sms_code)

    return new_user



def generate_otp():
    return str(random.randint(100000, 999999))

def generate_verification_code(user_id: int, db: Session, verification_type: str):
    code = generate_otp()
    expiration = datetime.utcnow() + timedelta(minutes=1)  # OTP valid for 1 minutes
    
    verification_code = VerificationCode(
        token=code,   # storing 6-digit code
        expiration=expiration,
        user_id=user_id,
        type=verification_type
    )
    
    db.add(verification_code)
    db.commit()
    
    return code
def send_verification_email(email: str, code: str):
    message = MIMEText(f"Your verification code is: {code}\nThis code expires in 10 minutes.")
    message['Subject'] = 'Email Verification Code'
    message['From'] = EMAIL_USER
    message['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(message)
    # except Exception as e:
    #     print(f"Failed to send email: {e}")


def send_verification_sms(phone_number: str, token: str):
    pass
    # verification_link = f"http://yourapp.com/verify/{token}"
    # message_body = f"Please verify your phone number by clicking the following link: {verification_link}"

    # # Twilio setup
    # account_sid = 'your_twilio_account_sid'
    # auth_token = 'your_twilio_auth_token'
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     body=message_body,
    #     from_='your_registered_sender_id',  # Replace with your registered Sender ID
    #     to=phone_number
    # )

    # return message
