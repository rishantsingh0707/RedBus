import uuid
from sqlalchemy import Column, String, TIMESTAMP, Integer
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    google_Id = Column(String(255), unique=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(String(20))
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    @property
    def first_name(self) -> str:
        if not self.full_name:
            return ""
        return self.full_name.split(" ", 1)[0]

    @property
    def last_name(self) -> str:
        if not self.full_name:
            return ""
        parts = self.full_name.split(" ", 1)
        if len(parts) == 1:
            return ""
        return parts[1]
