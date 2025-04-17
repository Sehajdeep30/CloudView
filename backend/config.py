# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
DATABASE_URL = os.getenv("DATABASE_URL")
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
IS_HTTPS = False 
STACK_NAME = os.getenv("STACK_NAME")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
TEMPLATE_URL = os.getenv("TEMPLATE_URL")
