import traceback
from fastapi import APIRouter, HTTPException, Security, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
import datetime
from auth.auth import AuthHandler  # Import the authentication handler
from db.db import session  # Import the shared database session
from models.user_models import UserInput, User, UserLogin  # Import user models and schemas
from repos.user_repos import select_all_users, find_user  # Import repository functions for user operations
from config import *


# Create an instance of APIRouter for user endpoints
user_router = APIRouter()
# Create an instance of AuthHandler to manage authentication tasks
auth_handler = AuthHandler()

@user_router.post('/registration', status_code=HTTP_201_CREATED, tags=['users'],
                  description='Register new user')
def register(user: UserInput):
    """
    Register a new user.
    - Checks if the username is already taken.
    - Hashes the provided password.
    - Saves the new user to the database.
    """
    try:
        users = select_all_users()  # Retrieve all existing users
        if any(x.username == user.username for x in users):
            raise HTTPException(status_code=400, detail='Username is taken')
        hashed_pwd = auth_handler.get_password_hash(user.password)  # Hash the password
        # Create a new User object; 🔹 CUSTOMIZE fields as necessary
        u = User(username=user.username, password=hashed_pwd, email=user.email,created_at= datetime.datetime.now(datetime.timezone.utc))
        session.add(u)
        session.commit()
        return JSONResponse(status_code=HTTP_201_CREATED, content={"message": "User registered successfully"})
    except Exception as e:
        print("ERROR:", str(e))  # Print error message
        traceback.print_exc()  # Print full stack trace
        raise HTTPException(status_code=400, detail=str(e))

@user_router.post('/login', tags=['users'])
def login(user: UserLogin):
    """
    Authenticate a user.
    - Verifies username and password.
    - Returns a JWT token if authentication is successful.
    """
    try:
        user_found = find_user(user.username)
        if not user_found:
            raise HTTPException(status_code=401, detail='Invalid username and/or password')
        verified = auth_handler.verify_password(user.password, user_found.password)
        if not verified:
            raise HTTPException(status_code=401, detail='Invalid username and/or password')
        access_token = auth_handler.encode_access_token(user_found.username)
        refresh_token = auth_handler.encode_refresh_token(user_found.username)
        
        response = JSONResponse(content={"token_type": "bearer"})
        
        response.set_cookie(
            key="access_token", 
            value=access_token,
            httponly=True,
            secure=True,    # Use secure=True when in production over HTTPS
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # e.g., 15 minutes
            samesite="Lax"
        )
        response.set_cookie(
            key="refresh_token", 
            value=refresh_token, 
            httponly=True,   # Cookie is not accessible via JavaScript
            secure=True,     # Make sure it works only over HTTPS
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # Expiry period in days
            # same_site="strict"  # Prevents CSRF attacks   
        )
    except Exception as e:
        print("ERROR:", str(e))  # Print error message
        traceback.print_exc()  # Print full stack trace
        raise HTTPException(status_code=500, detail=str(e))
    return response

@user_router.post("/refresh", tags=['users'])
def refresh_token(refresh_token: str):
    """Generate a new access token using a valid refresh token."""
    try:
        user_id = auth_handler.decode_token(refresh_token)  # Decode the refresh token
        new_access_token = auth_handler.encode_access_token(user_id)
        response = JSONResponse(content={"token_type": "bearer"})
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite="Lax"
        )
        return response
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@user_router.get('/users/me', tags=['users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    """
    Retrieve the currently authenticated user.
    """
    return user

@user_router.post("/users/logout", tags=["users"])
def logout(response: Response):
    """
    Logs out the user by clearing the refresh token cookie.
    """
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="refresh_token", httponly=True, secure=True)
    return response