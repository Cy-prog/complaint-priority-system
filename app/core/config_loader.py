import yaml
from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel, Field
from typing import Dict, List

# Define models
class PriorityWeights(BaseModel):
    urgency: float
    severity: float
    impact: float
    safety: float
    duration: float

class SLAPolicy(BaseModel):
    response_hours: int
    resolution_hours: int

class EscalationRules(BaseModel):
    auto_escalate_on_breach: bool
    max_escalation_level: str
    escalation_step: int

class PriorityConfig(BaseModel):
    priority_weights: PriorityWeights
    priority_thresholds: Dict[str, int]
    sla_policies: Dict[str, SLAPolicy]
    confidence_thresholds: Dict[str, float]
    escalation_rules: EscalationRules

class CategoryDef(BaseModel):
    name: str
    description: str
    risk_level: str
    is_essential_service: bool
    department: str
    keywords: List[str]

class CategoriesConfig(BaseModel):
    categories: List[CategoryDef]

class DurationKeywords(BaseModel):
    hours: List[str]
    days: List[str]
    weeks: List[str]
    months: List[str]
    years: List[str]
    since_yesterday: List[str]
    since_morning: List[str]
    since_last_week: List[str]

class SafetyConfig(BaseModel):
    critical_safety_keywords: List[str]
    high_safety_keywords: List[str]
    vulnerable_population_keywords: List[str]
    escalation_signal_keywords: List[str]
    essential_service_disruption_keywords: List[str]
    duration_keywords: DurationKeywords

# Loaders
def _load_yaml(filename: str) -> dict:
    base_dir = Path(__file__).resolve().parent.parent.parent
    file_path = base_dir / "config" / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@lru_cache()
def load_priority_config() -> PriorityConfig:
    data = _load_yaml("priority_config.yaml")
    return PriorityConfig(**data)

@lru_cache()
def load_categories_config() -> CategoriesConfig:
    data = _load_yaml("categories.yaml")
    return CategoriesConfig(**data)

@lru_cache()
def load_safety_config() -> SafetyConfig:
    data = _load_yaml("safety_keywords.yaml")
    return SafetyConfig(**data)
