import traceback
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from models.aws_cred_models import UserAWSRole,UserAWSRoleInput
from models.user_models import User
from auth.auth import AuthHandler
from repos.aws_cred_repos import get_aws_role,set_aws_credentials
from aws_manager.aws_core_manager import AwsHandler
from config import *


# Create an instance of APIRouter for user endpoints
aws_router = APIRouter()
auth_handler = AuthHandler()
aws_handler = AwsHandler()

@aws_router.get('/loading_aws_data', status_code=HTTP_200_OK, tags=['aws_cred'],
                  description='Loading aws account credentials based on user id')
def load_aws_data(user: User = Depends(auth_handler.get_current_user)):
    """
    loads up server aws account information.
    Also checks if the user arn is already connected or not
    """
    try:
        user_aws_role = get_aws_role(user.id)
        if(user_aws_role):
            aws_handler.set_aws_role(user.id, user_aws_role.role_arn, user_aws_role.policies)
            return {"isUserAwsHandlerSet": True}
        else:
            return {"isUserAwsHandlerSet": False}
    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Could not load AWS data")

    
@aws_router.post('/set_aws_data', status_code=HTTP_201_CREATED, tags=['aws_cred'],
                  description='Setting up aws account credentials using user input')
def set_aws_data(aws_credentials:UserAWSRoleInput,user: User = Depends(auth_handler.get_current_user)):
    """
    Takes in user data.
    Adds their aws access credentials to database
    """
    try:
        aws_handler.set_aws_role(user.id,aws_credentials.role_arn,aws_credentials.policy_arns)
        creds = UserAWSRole(user_id=user.id,role_arn=aws_handler.role_arn,policies=aws_handler.policies)
        set_aws_credentials(creds)
        return {"message": "AWS Role Credentials Added Successfully"}
    except Exception as e:
        aws_handler.remove_aws_role()
        print("ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to set AWS credentials")
    