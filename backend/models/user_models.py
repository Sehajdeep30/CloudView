import datetime  # For timestamping user creation
from typing import Optional
from pydantic import field_validator, EmailStr,ValidationInfo # For email validation and custom validators
from sqlmodel import SQLModel, Field, Relationship

# SQLModel for User; represents the users table in the database
class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)  
    username: str = Field(index=True)  
    password: str = Field(max_length=256, min_length=6)  
    email: EmailStr 
    # Automatically set created_at to the current datetime when a user is created
    created_at: datetime.datetime = datetime.datetime.now()

# Model for user input during registration; not stored directly in DB
class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str  # Confirmation for password
    email: EmailStr

    # Validator to ensure password and password2 match

    @field_validator("password2")
    def password_match(cls, v, values: ValidationInfo):
        if 'password' in values.data and v != values.data['password']:
            raise ValueError('Passwords do not match')
            return v

# Model for user login (only requires username and password)
class UserLogin(SQLModel):
    username: str
    password: str