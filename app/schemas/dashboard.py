from pydantic import BaseModel
from typing import List

class DashboardSummary(BaseModel):
    total_complaints: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    pending_count: int
    open_count: int
    in_progress_count: int
    resolved_count: int
    avg_resolution_time_hours: float
    sla_breach_count: int
    duplicate_count: int
    avg_confidence: float

class TrendData(BaseModel):
    date: str
    count: int

class CategoryDistribution(BaseModel):
    category: str
    count: int

class PriorityDistribution(BaseModel):
    priority: str
    count: int

class AnalyticsResponse(BaseModel):
    complaints_over_time: List[TrendData]
    priority_distribution: List[PriorityDistribution]
    category_distribution: List[CategoryDistribution]
    override_rate: float
    avg_confidence: float
    sla_compliance_rate: float
