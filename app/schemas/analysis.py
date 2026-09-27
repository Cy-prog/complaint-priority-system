"""Pydantic schemas for AI analysis responses."""

from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class AnalysisResponse(BaseModel):
    """Response schema for complaint analysis results."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    complaint_id: int
    priority: str
    priority_score: int
    urgency_score: int
    severity_score: int
    impact_score: int
    safety_score: int
    duration_score: int
    confidence: float
    sentiment: Optional[str] = None
    risk_level: Optional[str] = None
    entities: Optional[Any] = None
    key_issues: Optional[list] = None
    affected_population: Optional[str] = None
    affected_population_estimate: Optional[int] = None
    reasoning_summary: Optional[str] = None
    recommended_action: Optional[str] = None
    duplicate_probability: float = 0.0
    analysis_model_version: Optional[str] = None
    analysis_latency_ms: Optional[float] = None
    analyzed_at: Optional[datetime] = None


class PriorityOverrideRequest(BaseModel):
    """Request schema for overriding AI priority."""
    new_priority: str
    new_score: Optional[int] = None
    reason: str


class PriorityOverrideResponse(BaseModel):
    """Response schema for priority override result."""
    id: int
    original_priority: str
    original_score: Optional[int] = None
    new_priority: str
    new_score: Optional[int] = None
    reason: str
    changed_at: datetime
    changed_by_username: str


class FeedbackRequest(BaseModel):
    """Request schema for submitting correction feedback."""
    feedback_type: str
    original_value: str
    corrected_value: str
    reason: str


class FeedbackResponse(BaseModel):
    """Response schema for feedback submission."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    feedback_type: str
    original_value: str
    corrected_value: str
    reason: str
    used_for_training: bool = False
    created_at: Optional[datetime] = None


class SimilarComplaintResponse(BaseModel):
    """Response schema for similar/duplicate complaints."""
    complaint_id: str
    complaint_text: str
    similarity_score: float
    category: Optional[str] = None
    priority: Optional[str] = None


class ExplanationResponse(BaseModel):
    """Detailed AI explanation with per-dimension breakdown."""
    reasoning_summary: str
    recommended_action: str
    dimension_explanations: dict[str, str] = {}
