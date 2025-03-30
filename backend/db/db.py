from sqlmodel import create_engine
from sqlmodel import Session

# Specify the name of the PostgreSQL database file
eng = 'cloudviewdb.db'

# Construct the PostgreSQL URL
db_url = f'postgresql://postgres:OEE*0Rb^@localhost:5432{eng}'

# Create the database engine with echo enabled for SQL logging
engine = create_engine(db_url)

# Create a Session object bound to the engine for database operations
session = Session(bind=engine)