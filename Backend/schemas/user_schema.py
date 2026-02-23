from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=4)
    phone: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)


class GoogleLoginRequest(BaseModel):
    id_token: str = Field(min_length=10)


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
