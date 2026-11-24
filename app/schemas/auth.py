"""Pydantic schemas for authentication."""

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    """Login credentials."""
    username: str
    password: str

class RegisterRequest(BaseModel):
    """Citizen registration data."""
    username: str
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None

class UserResponse(BaseModel):
    """User information response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    phone: Optional[str] = None
    department_id: Optional[int] = None
    is_active: bool

class LoginResponse(BaseModel):
    """Login success response."""
    token: str
    user: UserResponse
