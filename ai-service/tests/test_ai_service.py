import pytest
import sys
from pathlib import Path

# Add project root and ai-service to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BASE_DIR))

from app import app, API_KEY

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ─── 1. Health & Auth ──────────────────────────────────────────
def test_health_check(client):
    response = client.get("/ai/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"
    assert "version" in data

def test_unauthorized_access(client):
    response = client.get("/ai/model/status")
    assert response.status_code == 401

def test_model_status_and_metrics(client):
    res_status = client.get("/ai/model/status", headers={"X-API-Key": API_KEY})
    assert res_status.status_code == 200
    status_data = res_status.get_json()
    assert status_data["status"] == "active"
    assert status_data["pipelineStages"] == 19
    assert status_data["evaluationAccuracy"] >= 0.85

    res_metrics = client.get("/ai/model/metrics", headers={"X-API-Key": API_KEY})
    assert res_metrics.status_code == 200
    metrics_data = res_metrics.get_json()
    assert metrics_data["accuracy"] >= 0.85
    assert metrics_data["totalDatasetSamples"] >= 500

# ─── 2. Hit-and-Run Benchmark Test Case ────────────────────────
def test_hit_and_run_benchmark(client):
    payload = {
        "description": (
            "A black SUV hit a pedestrian near the railway station around 8:30 PM and escaped "
            "toward the highway. The person appears to be injured. I could only see part of the number plate MP07 AB 2."
        )
    }
    response = client.post("/ai/analyze", json=payload, headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    data = response.get_json()

    assert data["category"] == "Public Safety"
    assert data["incidentType"] == "HIT_AND_RUN"
    assert data["vehicle"]["type"] == "SUV"
    assert data["vehicle"]["color"] == "BLACK"
    assert "MP07 AB 2" in data["vehicle"]["plate"]
    assert "20:30" in data["approximateTime"]
    assert data["direction"] == "highway"
    assert data["injuryReported"] is True
    assert data["priority"] == "CRITICAL"
    assert data["priorityScore"] >= 75
    assert data["categoryConfidence"] > 0.80
    assert data["priorityConfidence"] > 0.80
    assert "injury reported" in data["reasons"]
    assert "active hit-and-run incident" in data["reasons"]

# ─── 3. Domain Categories: Road, Water, Elec, Garbage, Sanitation, Parks, Fire, Theft, Medical ─
@pytest.mark.parametrize("description,expected_cat,min_priority,expected_incident", [
    ("Massive deep pothole on the main road causing car accidents and traffic jam.", "Roads", "MEDIUM", "GENERAL"),
    ("Drinking water pipeline burst and flooding street, yellow dirty water coming in taps.", "Water Supply", "MEDIUM", "GENERAL"),
    ("High voltage transformer exploded with loud blast and sparks near market.", "Electricity", "CRITICAL", "CIVIC_HAZARD"),
    ("Overflowing rotten garbage dump outside school gate not cleared for 2 weeks.", "Garbage/Waste", "MEDIUM", "GENERAL"),
    ("Open manhole on footpath with no cover or warning, extreme falling hazard.", "Sanitation", "CRITICAL", "CIVIC_HAZARD"),
    ("Children swings and slides broken with rusted sharp iron edges in public garden.", "Parks", "LOW", "GENERAL"),
    ("Huge fire blazing in furniture warehouse, smoke billowing rapidly.", "Public Safety", "CRITICAL", "FIRE"),
    ("Armed robbery at shop, thieves had guns and fled on red motorbike.", "Public Safety", "CRITICAL", "ARMED_ROBBERY"),
    ("Civil hospital emergency has no oxygen cylinders or doctors for dying patients.", "Public Health", "CRITICAL", "MEDICAL_EMERGENCY"),
])
def test_domain_categories(client, description, expected_cat, min_priority, expected_incident):
    res = client.post("/ai/analyze", json={"description": description}, headers={"X-API-Key": API_KEY})
    assert res.status_code == 200
    data = res.get_json()
    assert data["category"] in [expected_cat, "Healthcare", "Public Health"]
    if min_priority == "CRITICAL":
        assert data["priority"] == "CRITICAL"
    assert len(data["reasons"]) > 0

# ─── 4. Linguistic Variations: Hindi, Hinglish, Misspelled, Short, Long, Ambiguous ─
def test_hindi_complaint(client):
    payload = {"description": "काले रंग की गाड़ी ने टक्कर मार दी और भाग गया, व्यक्ति गंभीर रूप से घायल है।"}
    res = client.post("/ai/analyze", json=payload, headers={"X-API-Key": API_KEY})
    assert res.status_code == 200
    data = res.get_json()
    assert data["category"] == "Public Safety"
    assert data["priority"] == "CRITICAL"
    assert data["injuryReported"] is True

def test_hinglish_complaint(client):
    payload = {"description": "Pichle 4 din se hamare area me paani ki supply band hai, residents bohot pareshan hain."}
    res = client.post("/ai/analyze", json=payload, headers={"X-API-Key": API_KEY})
    assert res.status_code == 200
    data = res.get_json()
    assert data["category"] == "Water Supply"
    assert data["priority"] in ["HIGH", "CRITICAL"]

def test_misspelled_complaint(client):
    payload = {"description": "Electrcty transfomer blast on stret, light completly gone."}
    res = client.post("/ai/analyze", json=payload, headers={"X-API-Key": API_KEY})
    assert res.status_code == 200
    data = res.get_json()
    assert data["category"] == "Electricity"
    assert data["priority"] in ["HIGH", "CRITICAL"]

def test_short_complaint(client):
    payload = {"description": "Pothole"}
    res = client.post("/ai/analyze", json=payload, headers={"X-API-Key": API_KEY})
    assert res.status_code == 200
    data = res.get_json()
    assert data["category"] == "Roads"

def test_ambiguous_complaint(client):
    payload = {"description": "Something is wrong in our ward, please help immediately."}
    res = client.post("/ai/analyze", json=payload, headers={"X-API-Key": API_KEY})
    assert res.status_code == 200
    data = res.get_json()
    # Should not crash and assign modest priority
    assert data["category"] in ["Other", "Government Services"]
    assert data["priority"] in ["LOW", "MEDIUM"]

# ─── 5. Duplicate Complaint Detection ─────────────────────────
def test_duplicate_incident_detection(client):
    # Register complaint 101
    c1 = {
        "complaint_id": 101,
        "description": "Black SUV hit someone near railway station and fled."
    }
    client.post("/ai/analyze", json=c1, headers={"X-API-Key": API_KEY})

    # Register complaint 102 with related phrasing
    c2 = {
        "complaint_id": 102,
        "description": "Accident involving black SUV at railway station."
    }
    res2 = client.post("/ai/analyze", json=c2, headers={"X-API-Key": API_KEY})
    assert res2.status_code == 200
    data2 = res2.get_json()
    
    assert data2["duplicateProbability"] > 0.50
    assert 101 in data2["similarComplaintIds"]
    assert len(data2["similarIncidents"]) > 0
    assert "reason_for_similarity" in data2["similarIncidents"][0]
    assert data2["similarIncidents"][0]["auto_merged"] is False
    assert data2["similarIncidents"][0]["requires_officer_confirmation"] is True

# ─── 6. AI Robustness & Fallback Handling ─────────────────────
def test_empty_payload(client):
    res = client.post("/ai/analyze", json={}, headers={"X-API-Key": API_KEY})
    assert res.status_code == 200
    data = res.get_json()
    assert "priority" in data
    assert "category" in data

def test_malformed_json_fallback(client):
    res = client.post("/ai/analyze", data="bad-json", content_type="application/json", headers={"X-API-Key": API_KEY})
    assert res.status_code == 200
    data = res.get_json()
    assert "priority" in data
