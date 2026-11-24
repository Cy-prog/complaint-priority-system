import sys
from pathlib import Path
import importlib.util
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Load ai-service without polluting or shadowing top-level 'app' package
ai_service_path = BASE_DIR / "ai-service" / "app.py"
spec = importlib.util.spec_from_file_location("ai_microservice_app", ai_service_path)
ai_service_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai_service_module)

app = ai_service_module.app
API_KEY = ai_service_module.API_KEY

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
