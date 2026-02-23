import uuid
from sqlalchemy import Column, ForeignKey, TIMESTAMP, Numeric, Integer
from database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)

    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)

    departure_time = Column(TIMESTAMP, nullable=False)
    arrival_time = Column(TIMESTAMP, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
deleted_at = Column(TIMESTAMP, nullable=True)
