from sqlmodel import Session, select

from db.db import engine  # Import the database engine from the DB module
from models.user_models import User  # Import the User model

def select_all_users():
    """
    Retrieve all users from the database.
    Returns a list of User objects.
    """
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res

def find_user(name):
    """
    Find a user by username.
    Returns the first matching User object or None if not found.
    """
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()
    
def set_user(user):
    """
    Sets up the user in the database
    """
    
    with Session(engine) as session:
        session.add(user)
        session.commit()