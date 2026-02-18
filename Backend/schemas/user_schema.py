from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str

class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str

    class Config:
        from_attributes = True
