# import uuid
# from sqlalchemy import Column, ForeignKey, TIMESTAMP, Numeric
# from sqlalchemy.dialects.postgresql import UUID
# from database import Base

# class Schedule(Base):
#     __tablename__ = "schedules"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

#     bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id"), nullable=False)
#     route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False)

#     departure_time = Column(TIMESTAMP, nullable=False)
#     arrival_time = Column(TIMESTAMP, nullable=False)
#     price = Column(Numeric(10,2), nullable=False)
