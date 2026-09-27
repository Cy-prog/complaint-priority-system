from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class AnalysisResult:
    category: str
    subcategory: Optional[str]
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    priority_score: int  # 0-100
    urgency_score: int  # 0-100
    severity_score: int  # 0-100
    impact_score: int  # 0-100
    safety_score: int  # 0-100
    duration_score: int  # 0-100
    confidence: float  # 0.0-1.0
    sentiment: str  # positive, neutral, negative, very_negative
    risk_level: str  # low, medium, high, critical
    entities: List[Dict[str, Any]]
    key_issues: List[str]
    affected_population: Optional[str]
    affected_population_estimate: Optional[int]
    reasoning_summary: str
    recommended_action: str
    duplicate_probability: float
    similar_complaint_ids: List[int]
    language: str
    analysis_model_version: str
    analysis_latency_ms: float
    # Enhanced hybrid fields
    reasons: List[str] = field(default_factory=list)
    category_confidence: float = 0.85
    priority_confidence: float = 0.85
    sentiment_confidence: float = 0.75
    entity_confidence: float = 0.70
    disruption_score: int = 40
    vulnerability_score: int = 20
    incident_type: str = "GENERAL"
    vehicle: Dict[str, Any] = field(default_factory=dict)
    approximate_time: Optional[str] = None
    direction: Optional[str] = None
    injury_reported: bool = False
    similar_incidents: List[Dict[str, Any]] = field(default_factory=list)
    provenance: Dict[str, str] = field(default_factory=dict)
