from app.database import engine, Base
from app import models  # important

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("All tables created successfully!")
