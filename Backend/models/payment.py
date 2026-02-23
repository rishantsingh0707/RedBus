import uuid
from sqlalchemy import Column, ForeignKey, Numeric, String, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)

    amount = Column(Numeric(10,2), nullable=False)
    payment_status = Column(String(20), default="pending")
    transaction_id = Column(String(255))
    paid_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())