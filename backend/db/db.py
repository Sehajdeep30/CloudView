from sqlmodel import create_engine
from sqlmodel import Session

# Specify the name of the SQLite database file
eng = 'database.db'

# Construct the SQLite URL (for PostgreSQL, update this URL accordingly)
sqlite_url = f'sqlite:///{eng}'

# Create the database engine with echo enabled for SQL logging
engine = create_engine(sqlite_url, echo=True)

# Create a Session object bound to the engine for database operations
session = Session(bind=engine)