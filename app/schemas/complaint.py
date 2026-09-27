"""Pydantic schemas for complaint CRUD operations."""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from .analysis import AnalysisResponse


class ComplaintCreate(BaseModel):
    """Schema for creating a new complaint."""
    complaint_text: str = Field(..., min_length=10, max_length=5000)
    complainant_name: Optional[str] = None
    complainant_contact: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    area: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ComplaintUpdate(BaseModel):
    """Schema for updating an existing complaint."""
    status: Optional[str] = None
    category_id: Optional[int] = None
    assigned_department_id: Optional[int] = None
    assigned_user_id: Optional[int] = None


class CategoryResponse(BaseModel):
    """Schema for category in responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    risk_level: Optional[str] = None
    is_essential_service: bool = False


class DepartmentResponse(BaseModel):
    """Schema for department in responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class SLARecordResponse(BaseModel):
    """Schema for SLA record in responses."""
    model_config = ConfigDict(from_attributes=True)

    priority: str
    sla_deadline: datetime
    is_breached: bool = False
    response_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    response_time_minutes: Optional[int] = None
    resolution_time_minutes: Optional[int] = None


class ComplaintResponse(BaseModel):
    """Full complaint response with nested analysis, category, department, SLA."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_id: str
    complaint_text: str
    complainant_name: Optional[str] = None
    complainant_contact: Optional[str] = None
    language: Optional[str] = None
    status: str
    state: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    area: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    category_id: Optional[int] = None
    assigned_department_id: Optional[int] = None
    assigned_user_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    analysis: Optional[AnalysisResponse] = None
    category: Optional[CategoryResponse] = None
    assigned_department: Optional[DepartmentResponse] = None
    sla_record: Optional[SLARecordResponse] = None


class ComplaintListResponse(ComplaintResponse):
    """Complaint list item (same as full response for now)."""
    pass


class ComplaintFilters(BaseModel):
    """Query parameters for filtering complaints."""
    priority: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    city: Optional[str] = None
    ward: Optional[str] = None
    search: Optional[str] = None
