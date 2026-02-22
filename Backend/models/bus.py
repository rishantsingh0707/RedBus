# import uuid
# from sqlalchemy import Column, String, Integer, ForeignKey, JSON
# from sqlalchemy.dialects.postgresql import UUID
# from database import Base

# class Bus(Base):
#     __tablename__ = "buses"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

#     operator_id = Column(UUID(as_uuid=True), ForeignKey("operators.id"), nullable=False)

#     bus_number = Column(String(50), unique=True, nullable=False)
#     bus_type = Column(String(50), nullable=False)
#     total_seats = Column(Integer, nullable=False)

#     amenities = Column(JSON)
