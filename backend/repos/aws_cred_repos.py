from sqlmodel import Session, select
from db.db import engine
from models.aws_cred_models import UserAWSRole

def get_aws_role(user_id):
    """
    Gets the user aws role setup for the user. 
    """
    with Session(engine) as session:
        statement = select(UserAWSRole).where(UserAWSRole.user_id == user_id)
        user_aws_role = session.exec(statement).first()
        return user_aws_role

def set_aws_credentials(creds):
    """
    Sets up the user in the database
    """
    
    with Session(engine) as session:
        session.add(creds)
        session.commit()