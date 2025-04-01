from datetime import datetime,timezone  # For handling token expiry times

from fastapi import Security, HTTPException  # FastAPI components for security and error handling
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # For bearer token extraction
from passlib.context import CryptContext  # For password hashing and verification
import jwt  # For encoding and decoding JWT tokens
from starlette import status  # For HTTP status codes
from config import *

from repos.user_repos import find_user  # Custom repository function to retrieve a user from storage

# AuthHandler encapsulates all authentication related functions
class AuthHandler:
    # Initialize HTTPBearer for extracting token from request headers
    security = HTTPBearer()
    # Create a password context with bcrypt scheme for secure password hashing
    pwd_context = CryptContext(schemes=['bcrypt'])

    def get_password_hash(self, password):
        """Hash the plain text password using bcrypt."""
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        """Verify a plain text password against the hashed version."""
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_access_token(self, user_id):
        """Generate an access token."""
        payload = {
            'exp': datetime.now(timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=HASH_ALGORITHM)

    def encode_refresh_token(self, user_id):
        """Generate the refresh token."""
        payload = {
            'exp': datetime.now(timezone.utc) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=HASH_ALGORITHM)

    def decode_token(self, token):
        """
        Decode a JWT token.
        Raises an HTTPException if the token is expired or invalid.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired signature')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """ 
        Wrapper function that decodes the JWT token from the credentials.
        """
        return self.decode_token(auth.credentials)

    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """
        Retrieve the current user by decoding the token and then using the username to fetch user data.
        Raises an exception if credentials cannot be validated or the user is not found.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )
        username = self.decode_token(auth.credentials)
        if username is None:
            raise credentials_exception
        user = find_user(username)
        if user is None:
            raise credentials_exception
        return user