from sqlmodel import create_engine
from sqlmodel import Session
from config import *

# Specify the name of the PostgreSQL database file
eng = 'cloudviewdb.db'

# Construct the PostgreSQL URL
db_url = f'DATABASE_URL/{eng}'

# Create the database engine with echo enabled for SQL logging
engine = create_engine(db_url)

# Create a Session object bound to the engine for database operations
session = Session(bind=engine)