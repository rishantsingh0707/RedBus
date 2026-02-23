import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey,TIMESTAMP, Integer
from database import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)

    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)

    seat_number = Column(String(10), nullable=False)
    is_booked = Column(Boolean, default=False)
deleted_at = Column(TIMESTAMP, nullable=True)
