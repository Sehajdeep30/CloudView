# models/aws_models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field

class UserAWSRole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    role_arn: str
    policies: str

class UserAWSRoleInput(SQLModel):
    role_arn: str
    policy_arns: Optional[List[str]]
