
# models/auth_models.py
import uuid
from uuid import UUID
from fastapi import Form
from typing import Optional , List
from datetime import datetime
from pydantic import BaseModel, Field, BaseModel, EmailStr
# from response.user_response import User_Response
from fastapi.middleware.cors import CORSMiddleware

# class UserCreate(BaseModel):
#     first_name: str
#     last_name: str
#     email: EmailStr
#     password: str
#     phone: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str  # Add this line


class TokenData(BaseModel):
    username: str | None = None
    email: str | None = None

class UserRegistrationResponse(BaseModel):
    user: UserResponse
    message: str



class UserCreate(BaseModel):
    email: str
    password: str
    phone_number: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


