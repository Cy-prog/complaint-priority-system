from enum import Enum
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from fastapi import HTTPException, status, Depends
from config.settings import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

class Role(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_session_token(data: dict) -> str:
    return serializer.dumps(data)

def verify_session_token(token: str) -> dict | None:
    try:
        return serializer.loads(token, max_age=settings.SESSION_EXPIRY_HOURS * 3600)
    except Exception:
        return None

def require_role(required_role: str):
    def role_checker(user_role: str = "viewer"): # In reality, get user role from context
        if required_role == Role.ADMIN and user_role != Role.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        # Extend logic as needed
        return user_role
    return role_checker
