import uuid
from sqlalchemy import Column, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False)

    amount = Column(Numeric(10,2), nullable=False)
    payment_status = Column(String(20), default="pending")
    transaction_id = Column(String(255))
    paid_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, server_default=func.now())
