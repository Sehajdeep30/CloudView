from datetime import datetime,timezone  # For handling token expiry times

from fastapi import Security, HTTPException  # FastAPI components for security and error handling
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # For bearer token extraction
from passlib.context import CryptContext  # For password hashing and verification
import jwt  # For encoding and decoding JWT tokens
from starlette import status  # For HTTP status codes

from repos.user_repos import find_user  # Custom repository function to retrieve a user from storage

# AuthHandler encapsulates all authentication related functions
class AuthHandler:
    # Initialize HTTPBearer for extracting token from request headers
    security = HTTPBearer()
    # Create a password context with bcrypt scheme for secure password hashing
    pwd_context = CryptContext(schemes=['bcrypt'])
    # Secret key used for JWT encoding/decoding;
    secret = 'secret-key-CloudView'     '''*********Make It Secure*********'''

    def get_password_hash(self, password):
        """Hash the plain text password using bcrypt."""
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        """Verify a plain text password against the hashed version."""
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(self, user_id):
        """
        Encode a JWT token with an expiration time.
        'exp' - expiration time (current UTC time + 8 hours)
        'iat' - issued at time (current UTC time)
        'sub' - subject (user id)
        """
        payload = {
            'exp': datetime.now(timezone.utc) + datetime.timedelta(hours=8),
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        """
        Decode a JWT token.
        Raises an HTTPException if the token is expired or invalid.
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired signature')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """
        Wrapper function that decodes the JWT token from the credentials.
        This function can be used as a dependency in route handlers.
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