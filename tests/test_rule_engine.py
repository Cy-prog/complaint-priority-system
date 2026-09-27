import pytest
from ai.rule_engine import RuleEngine

@pytest.fixture
def rule_engine():
    return RuleEngine()

def test_critical_life_safety_override(rule_engine):
    analysis = {
        "priority": "LOW",
        "safety_score": 20,
        "entities": {
            "safety_hazards": ["live wire"],
            "vulnerable_groups": [],
            "durations": []
        }
    }
    result = rule_engine.apply_rules(analysis)
    assert result["priority"] == "CRITICAL"
    assert any("Rule 4" in r for r in result["rules_applied"])

def test_vulnerable_population_essential_disruption_override(rule_engine):
    analysis = {
        "priority": "MEDIUM",
        "is_essential_service": True,
        "entities": {
            "essential_service_disrupted": True,
            "vulnerable_groups": ["elderly", "children"],
            "safety_hazards": [],
            "durations": [{"value": 2, "unit": "days", "raw": "2 days"}]
        }
    }
    result = rule_engine.apply_rules(analysis)
    assert result["priority"] == "CRITICAL"
    assert any("Rule 3b" in r for r in result["rules_applied"])

def test_rules_only_escalate_never_downgrade(rule_engine):
    analysis = {
        "priority": "CRITICAL",
        "safety_score": 0,
        "entities": {
            "safety_hazards": [],
            "vulnerable_groups": [],
            "durations": []
        }
    }
    result = rule_engine.apply_rules(analysis)
    assert result["priority"] == "CRITICAL"
