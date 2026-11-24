from enum import Enum
import os
import uuid
import re
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from fastapi import HTTPException, status, UploadFile
from config.settings import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    DEPARTMENT_ADMIN = "department_admin"
    OFFICER = "officer"
    CITIZEN = "citizen"
    
    # Legacy backward-compatible aliases
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"

ROLE_HIERARCHY = {
    Role.SUPER_ADMIN.value: 4,
    Role.ADMIN.value: 4,
    Role.DEPARTMENT_ADMIN.value: 3,
    Role.OFFICER.value: 2,
    Role.OPERATOR.value: 2,
    Role.CITIZEN.value: 1,
    Role.VIEWER.value: 1
}

def normalize_role(role: str) -> str:
    """Normalize legacy role identifiers to canonical major project roles."""
    if not role:
        return Role.CITIZEN.value
    r = str(role).strip().lower()
    if r in ("admin", "super_admin", "superadmin"):
        return Role.SUPER_ADMIN.value
    if r in ("department_admin", "dept_admin", "deptadmin"):
        return Role.DEPARTMENT_ADMIN.value
    if r in ("operator", "officer", "field_officer"):
        return Role.OFFICER.value
    return Role.CITIZEN.value

def has_role(user_role: str, required_role: str) -> bool:
    """Check if user role has sufficient privileges in the RBAC hierarchy."""
    user_level = ROLE_HIERARCHY.get(normalize_role(user_role), 1)
    required_level = ROLE_HIERARCHY.get(normalize_role(required_role), 1)
    return user_level >= required_level

def is_role_in(user_role: str, allowed_roles: list[str]) -> bool:
    """Check if user role matches or is contained in an explicit whitelist of roles."""
    norm_user = normalize_role(user_role)
    norm_allowed = [normalize_role(r) for r in allowed_roles]
    return norm_user in norm_allowed or norm_user == Role.SUPER_ADMIN.value

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

# Safe file upload validation
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

def validate_and_sanitize_upload(filename: str, content: bytes, content_type: str | None = None) -> str:
    """
    Validates file extension, MIME type, and size to prevent remote execution / disk exhaustion.
    Returns safe unique filename.
    """
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Uploaded file exceeds maximum allowed size ({MAX_FILE_SIZE_BYTES // (1024*1024)} MB)"
        )
    
    ext = os.path.splitext(filename or "")[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension '{ext}'. Allowed extensions: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}"
        )
        
    if content_type and content_type.lower() not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid MIME content type '{content_type}'."
        )

    # Magic byte check for images
    is_valid_magic = False
    if content.startswith(b'\xff\xd8\xff'):  # JPEG
        is_valid_magic = True
    elif content.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
        is_valid_magic = True
    elif content.startswith(b'RIFF') and b'WEBP' in content[:16]:  # WEBP
        is_valid_magic = True
        
    if not is_valid_magic and len(content) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content does not match genuine image signature."
        )

    unique_id = uuid.uuid4().hex[:12]
    return f"{unique_id}{ext}"
