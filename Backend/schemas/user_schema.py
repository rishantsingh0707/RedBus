from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str  # Add this line


class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None

class UserCreate(BaseModel):
    email: str
    password: str
    phone_number: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


