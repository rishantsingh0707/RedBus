import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "postgres",
    "database": "mybus",
    "port": 5432
}

EMAIL_USER= os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SECRET_KEY =  os.getenv('SECRET_KEY')
ALGORITHM =  os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # Default to 30 minutes if not set
REFRESH_TOKEN_EXPIRE_DAYS =  os.getenv('REFRESH_TOKEN_EXPIRE_DAYS')

