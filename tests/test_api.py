import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "ai-service"))

from app import app, API_KEY

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_flask_health_check(client):
    response = client.get("/ai/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"

def test_flask_model_metrics(client):
    response = client.get("/ai/model/metrics", headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    data = response.get_json()
    assert "accuracy" in data
    assert "f1_score" in data

def test_flask_analyze_pipeline(client):
    payload = {
        "description": "Exposed high voltage electrical wire sparking in front of school gate.",
        "city": "Mumbai",
        "ward": "15"
    }
    response = client.post("/ai/analyze", json=payload, headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    data = response.get_json()
    assert data["priority"] == "CRITICAL"
    assert data["priorityScore"] >= 0.70

def test_flask_quick_scan(client):
    payload = {"text": "Live sparking electrical wire on road near school"}
    response = client.post("/ai/quick-scan", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["priority"] == "CRITICAL"
    assert "category" in data
    assert data["confidence"] > 0

