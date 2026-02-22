# import uuid
# from sqlalchemy import Column, String, Boolean, ForeignKey
# from sqlalchemy.dialects.postgresql import UUID
# from database import Base

# class Seat(Base):
#     __tablename__ = "seats"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

#     schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False)

#     seat_number = Column(String(10), nullable=False)
#     is_booked = Column(Boolean, default=False)
