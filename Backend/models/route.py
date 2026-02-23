import uuid
from sqlalchemy import Column, Integer, ForeignKey, Interval,TIMESTAMP
from database import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    source_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    destination_city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    distance_km = Column(Integer)
    estimated_duration = Column(Interval)
    deleted_at = Column(TIMESTAMP, nullable=True)

