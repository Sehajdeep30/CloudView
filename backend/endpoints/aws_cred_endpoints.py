import traceback
from fastapi import APIRouter, HTTPException, Depends,Body, Response, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from models.aws_cred_models import UserAWSRole,UserAWSRoleInput
from models.user_models import User
from auth.auth import AuthHandler
from repos.aws_cred_repos import get_aws_role,set_aws_credentials,update_aws_credentials
from aws_manager.aws_core_manager import AwsHandler
from botocore.exceptions import ClientError
from config import *


# Create an instance of APIRouter for user endpoints
aws_router = APIRouter()
auth_handler = AuthHandler()

@aws_router.get('/aws_cred/status',
                status_code=HTTP_200_OK,
                tags=['aws_cred'],
                description= 'Check if AWS role is already connected for this user')

def load_aws_status(user: User = Depends(auth_handler.get_current_user)):
    """
    loads up server aws account information.
    Also checks if the user arn is already connected or not
    """
    try:
        is_aws_role = get_aws_role(user.id) is not None
        return {"isUserAwsHandlerSet": is_aws_role}
    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(500, "Could not load AWS connection status")
    
    
@aws_router.post('/aws_cred/launch_url',
                 tags=['aws_cred'],
                 description="This endpoint is used to create the launch URL")

def generate_stack_url(policy_arns: list[str] = Body(..., embed=True),
                       user: User = Depends(auth_handler.get_current_user),
                       aws: AwsHandler = Depends(AwsHandler.get_aws_handler)):
    """
    Generate a secure CloudFormation stack URL for the user with the provided policy ARNs.
    """
    try:
        launch_url = aws.set_template_url(user.id,policy_arns)
        return {"launch_url": launch_url}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to generate CloudFormation URL")
    
    
@aws_router.post('/aws_cred/add_role',
                  status_code=HTTP_201_CREATED,
                  tags=['aws_cred'],
                  description='Setting up aws account credentials using user input')

def set_aws_data(aws_credentials:UserAWSRoleInput,
                 user: User = Depends(auth_handler.get_current_user)):
    """
    Takes in user data.
    Adds their aws access credentials to database
    """
    try:
        policies = ",".join(aws_credentials.policy_arns)
        creds = UserAWSRole(user.id,aws_credentials.role_arn,policies)
        set_aws_credentials(creds)
        return {"message": "AWS Role Credentials Added Successfully"}
    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to set AWS credentials")
    
    
@aws_router.post('/aws_cred/update_role',
                 status_code=HTTP_201_CREATED, tags=['aws_cred'],
                  description='Updating aws account permissions')

def update_aws_data(policy_arns: list[str] = Body(..., embed=True),
                    user: User = Depends(auth_handler.get_current_user),
                    aws: AwsHandler = Depends(AwsHandler.get_aws_handler)):
    """
    Takes in upated user data.
    Updates their aws access credentials to database
    """
    try:
        aws.assume_role(user.id, None, None)  
        
        new_policy = aws.iam.update_iam_policy(user.id, policy_arns, aws.policies)
        if new_policy is not None:
            aws.policies = new_policy
            update_aws_credentials(user.id,new_policy)

        return {"message": "AWS Role Credentials Updated Successfully"}
    
    except ClientError as e:
        # AWS-side error (permissions, throttling, etc.)
        raise HTTPException(502, f"AWS API error: {e}")
    except ValueError as e:
        # e.g. no DB record to update
        raise HTTPException(404, str(e))
    except Exception as e:
        aws.remove_aws_role()
        traceback.print_exc()
        raise HTTPException(500, "Failed to update AWS credentials")