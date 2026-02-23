# import uuid
# from sqlalchemy import Column, Integer, ForeignKey, Interval
# from sqlalchemy.dialects.postgresql import UUID
# from database import Base

# class Route(Base):
#     __tablename__ = "routes"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

#     source_city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False)
#     destination_city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False)

#     distance_km = Column(Integer)
#     estimated_duration = Column(Interval)
