import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, JSON,TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)

    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    bus_number = Column(String(50), unique=True, nullable=False)
    bus_type = Column(String(50), nullable=False)
    total_seats = Column(Integer, nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    amenities = Column(JSON)
