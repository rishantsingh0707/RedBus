import random

def generate_otp():
    return random.randint(100000, 999999)

def send_sms(phone_number: str):
    otp = generate_otp()
    print(f"Sending SMS to {phone_number}")
    print(f"Your OTP is: {otp}")
    return {
        "phone": phone_number,
        "otp": otp,
        "status": "SMS Sent Successfully"
    }
