import pytest
from ai.pipeline import get_pipeline

@pytest.fixture(scope="module")
def pipeline():
    return get_pipeline()

def test_edge_case_positive_status(pipeline):
    # "Everything is fine now." -> Should be LOW priority
    res = pipeline.analyze("Everything is fine now.")
    assert res.priority == "LOW"

def test_edge_case_empty_urgency(pipeline):
    # "URGENT!!!" with no factual content -> Should NOT be CRITICAL
    res = pipeline.analyze("URGENT!!!")
    assert res.priority in ["LOW", "MEDIUM"]
    assert res.priority != "CRITICAL"

def test_edge_case_broken_streetlight(pipeline):
    # Low-risk infrastructure issue
    res = pipeline.analyze("There is a broken streetlight.")
    assert res.priority in ["LOW", "MEDIUM"]

def test_edge_case_exposed_wire_near_school(pipeline):
    # Life-safety hazard with vulnerable population -> MUST be CRITICAL
    res = pipeline.analyze("There is an exposed live electrical wire near a school.")
    assert res.priority == "CRITICAL"
    assert res.recommended_action != ""

def test_edge_case_extended_water_outage(pipeline):
    # Essential service unavailable for 5 days -> HIGH or CRITICAL
    res = pipeline.analyze("Water has been unavailable for 5 days.")
    assert res.priority in ["HIGH", "CRITICAL"]

def test_edge_case_repeated_report(pipeline):
    # Escalation signal present
    res = pipeline.analyze("Someone already reported this yesterday.")
    assert res.category is not None
