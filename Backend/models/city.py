# import uuid
# from sqlalchemy import Column, String
# from sqlalchemy.dialects.postgresql import UUID
# from database import Base

# class City(Base):
#     __tablename__ = "cities"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String(100), nullable=False)
#     state = Column(String(100))
