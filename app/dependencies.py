import os
from fastapi import Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.auth_service import AuthService
from app.models import User
from app.core.security import normalize_role, has_role, is_role_in, Role

templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)
templates.env.globals["get_flashed_messages"] = lambda *args, **kwargs: []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_templates():
    return templates

def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    token = request.cookies.get("session_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
    if not token:
        return None
    auth_service = AuthService()
    return auth_service.get_current_user(token, db)

def get_current_user(user: User | None = Depends(get_optional_user)) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to perform this action"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    return user

def require_roles(*allowed_roles: str):
    """Dependency factory checking whether current user belongs to one of the specified roles."""
    def role_dependency(user: User = Depends(get_current_user)) -> User:
        if not is_role_in(user.role, list(allowed_roles)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: Action requires one of roles {[r for r in allowed_roles]}. Current role: {user.role}"
            )
        return user
    return role_dependency

def get_current_citizen(user: User = Depends(get_current_user)) -> User:
    """Any authenticated user is at least a citizen."""
    return user

def get_current_officer(user: User = Depends(get_current_user)) -> User:
    if not has_role(user.role, Role.OFFICER.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires municipal officer or administrator credentials"
        )
    return user

def get_current_dept_admin(user: User = Depends(get_current_user)) -> User:
    if not has_role(user.role, Role.DEPARTMENT_ADMIN.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires department administrator or super administrator credentials"
        )
    return user

def get_current_super_admin(user: User = Depends(get_current_user)) -> User:
    if not has_role(user.role, Role.SUPER_ADMIN.value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires apex super administrator privileges"
        )
    return user

# Backward-compatible alias for existing endpoints
get_current_admin = get_current_super_admin
