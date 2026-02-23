# import uuid
# from sqlalchemy import Column, String, TIMESTAMP
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.sql import func
# from database import Base

# class Operator(Base):
#     __tablename__ = "operators"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String(150), nullable=False)
#     contact_email = Column(String(255))
#     contact_phone = Column(String(20))
#     deleted_at = Column(TIMESTAMP)
#     created_at = Column(TIMESTAMP, server_default=func.now())
