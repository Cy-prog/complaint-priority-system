"""Pydantic schemas for authentication."""

from pydantic import BaseModel, ConfigDict
from typing import Optional


class LoginRequest(BaseModel):
    """Login credentials."""
    username: str
    password: str


class UserResponse(BaseModel):
    """User information response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    is_active: bool


class LoginResponse(BaseModel):
    """Login success response."""
    token: str
    user: UserResponse
