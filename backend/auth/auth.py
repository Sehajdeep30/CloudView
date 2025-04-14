from datetime import datetime, timedelta, timezone  
from fastapi import HTTPException, Request, Depends  
from passlib.context import CryptContext  
import jwt  
from starlette import status  

from config import SECRET_KEY, HASH_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS  
from repos.user_repos import find_user  

class AuthHandler:
    """
    AuthHandler now uses HttpOnly cookies for access & refresh tokens.
    No more HTTPBearer header extraction.
    """

    pwd_context = CryptContext(schemes=['bcrypt'])  # bcrypt for password hashing

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return self.pwd_context.verify(plain, hashed)

    def encode_access_token(self, user_id: str) -> str:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=HASH_ALGORITHM)

    def encode_refresh_token(self, user_id: str) -> str:
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=HASH_ALGORITHM)

    def decode_token(self, token: str) -> str:
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
            return data['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired token')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def get_current_user(self, request: Request):
        """
        Dependency to inject the current user based on the 'access_token' cookie.
        """
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = self.decode_token(token)
        user = find_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
