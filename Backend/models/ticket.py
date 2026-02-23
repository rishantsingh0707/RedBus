import uuid
from sqlalchemy import Column, ForeignKey, String,TIMESTAMP,Integer
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    status = Column(String(20), default="booked")
deleted_at = Column(TIMESTAMP, nullable=True)
