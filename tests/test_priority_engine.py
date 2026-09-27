import pytest
from ai.priority_engine import PriorityEngine

@pytest.fixture
def engine():
    return PriorityEngine()

def test_priority_engine_low(engine):
    signals = {
        "category": "Streetlights",
        "category_risk_level": "low",
        "is_essential_service": False,
        "entities": {"safety_hazards": [], "vulnerable_groups": [], "durations": []},
        "sentiment": {"sentiment": "neutral"},
        "text_length": 50
    }
    res = engine.calculate_priority(signals)
    assert res["priority"] in ["LOW", "MEDIUM"]
    assert res["priority_score"] < 50

def test_priority_engine_high_urgency_essential(engine):
    signals = {
        "category": "Water Supply",
        "category_risk_level": "high",
        "is_essential_service": True,
        "entities": {
            "essential_service_disrupted": True,
            "safety_hazards": [],
            "vulnerable_groups": ["children", "elderly"],
            "durations": [{"value": 4, "unit": "days", "raw": "4 days"}],
            "people_affected_estimate": 100,
            "locations": ["Ward 5"]
        },
        "sentiment": {"sentiment": "negative"},
        "text_length": 120
    }
    res = engine.calculate_priority(signals)
    assert res["priority"] in ["HIGH", "CRITICAL"]
    assert res["urgency_score"] >= 70
    assert res["severity_score"] >= 60

def test_priority_engine_scores_bounded(engine):
    signals = {
        "category": "Electricity",
        "category_risk_level": "critical",
        "is_essential_service": True,
        "entities": {
            "safety_hazards": ["fire", "explosion", "electrocution", "live wire"],
            "vulnerable_groups": ["children", "hospital"],
            "durations": [{"value": 30, "unit": "days", "raw": "30 days"}],
            "people_affected_estimate": 500,
            "locations": ["Ward 1", "Ward 2", "Ward 3"]
        },
        "sentiment": {"sentiment": "very_negative"},
        "text_length": 300
    }
    res = engine.calculate_priority(signals)
    assert 0 <= res["priority_score"] <= 100
    assert 0 <= res["urgency_score"] <= 100
    assert 0 <= res["severity_score"] <= 100
    assert 0 <= res["impact_score"] <= 100
    assert 0 <= res["safety_score"] <= 100
    assert 0 <= res["duration_score"] <= 100
    assert res["priority"] == "CRITICAL"
