import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.main import app
from app.core.database import SessionLocal
from app.models import User, Complaint
from app.core.security import Role

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db():
    session = SessionLocal()
    yield session
    session.close()

def test_fastapi_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

def test_admin_login(client):
    res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    data = res.json()
    assert "token" in data
    assert data["user"]["username"] == "admin"
    assert data["user"]["role"] in ["super_admin", "admin"]

def test_citizen_registration_and_login(client):
    username = f"citizen_test_{pytest.__version__.replace('.', '')[:3]}"
    payload = {
        "username": username,
        "email": f"{username}@example.com",
        "password": "Password123!",
        "full_name": "Test Citizen User",
        "phone": "9998887776"
    }
    # Register
    reg_res = client.post("/api/auth/register", json=payload)
    assert reg_res.status_code in [201, 400]  # 400 if already created in earlier run
    
    # Login
    login_res = client.post("/api/auth/login", json={"username": username, "password": "Password123!"})
    assert login_res.status_code == 200
    assert login_res.json()["user"]["role"] == Role.CITIZEN.value

def test_complaint_creation_and_ai_analysis(client):
    # Login as admin
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create complaint
    payload = {
        "complaint_text": "Severe gas leak near hospital with sparking electric pole, immediate danger to patients.",
        "complainant_name": "Dr. Verma",
        "complainant_contact": "9876543210",
        "city": "Gwalior",
        "ward": "Ward 12",
        "area": "Hospital Gate",
        "latitude": 26.235,
        "longitude": 78.176
    }
    create_res = client.post("/api/complaints", json=payload, headers=headers)
    assert create_res.status_code == 200
    cmp_data = create_res.json()
    assert "complaint_id" in cmp_data
    assert cmp_data["status"] == "pending"
    assert cmp_data["latitude"] == 26.235

    cid = cmp_data["complaint_id"]

    # Trigger AI analysis
    analyze_res = client.post(f"/api/complaints/{cid}/analyze", headers=headers)
    assert analyze_res.status_code == 200
    analysis = analyze_res.json()
    assert analysis["priority"] == "CRITICAL"
    assert analysis["priority_score"] >= 75

def test_dashboard_summary_and_trends(client):
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Summary
    summary_res = client.get("/api/dashboard/summary", headers=headers)
    assert summary_res.status_code == 200
    summary = summary_res.json()
    assert summary["total_complaints"] > 0
    assert "critical_count" in summary
    assert "avg_confidence" in summary

    # Trends
    trends_res = client.get("/api/dashboard/trends?days=7", headers=headers)
    assert trends_res.status_code == 200
    trends = trends_res.json()
    assert isinstance(trends, list)
    assert len(trends) == 7

def test_file_upload_security_validation(client):
    from app.core.security import validate_and_sanitize_upload
    from fastapi import HTTPException

    # Valid PNG bytes
    valid_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + b"\x00" * 100
    safe_name = validate_and_sanitize_upload("test.png", valid_png, "image/png")
    assert safe_name.endswith(".png")

    # Invalid extension
    with pytest.raises(HTTPException) as excinfo:
        validate_and_sanitize_upload("malicious.exe", b"MZ\x90\x00", "application/octet-stream")
    assert excinfo.value.status_code == 400

    # Oversize file
    oversize_bytes = b"0" * (11 * 1024 * 1024)
    with pytest.raises(HTTPException) as excinfo:
        validate_and_sanitize_upload("huge.jpg", oversize_bytes, "image/jpeg")
    assert excinfo.value.status_code == 413


def test_department_and_workload_apis(client):
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # List departments
    depts_res = client.get("/api/departments", headers=headers)
    assert depts_res.status_code == 200
    depts = depts_res.json()
    assert isinstance(depts, list)
    assert len(depts) > 0

    dept_id = depts[0]["id"]
    # List officers for department
    officers_res = client.get(f"/api/departments/{dept_id}/officers", headers=headers)
    assert officers_res.status_code == 200
    officers = officers_res.json()
    assert isinstance(officers, list)


def test_sla_escalation_api(client):
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    esc_res = client.post("/api/sla/check-escalations", headers=headers)
    assert esc_res.status_code == 200
    data = esc_res.json()
    assert "escalated_count" in data


def test_gis_markers_api(client):
    res = client.get("/api/gis/markers")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    first_marker = data[0]
    assert "lat" in first_marker
    assert "lng" in first_marker


def test_predictive_forecast_api(client):
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    forecast_res = client.get("/api/predictive/forecast", headers=headers)
    assert forecast_res.status_code == 200
    fdata = forecast_res.json()
    assert "forecast" in fdata
    assert "days" in fdata
    assert len(fdata["days"]) == 14
    assert "confidence_level" in fdata


def test_transparency_api(client):
    res = client.get("/api/transparency/metrics")
    assert res.status_code == 200
    tdata = res.json()
    assert "total_complaints" in tdata
    assert "resolved_complaints" in tdata
    assert "resolution_percentage" in tdata


def test_report_exports(client):
    login_res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # CSV
    csv_res = client.get("/api/reports/csv", headers=headers)
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers.get("content-type", "")
    assert len(csv_res.content) > 50

    # Excel
    xlsx_res = client.get("/api/reports/excel", headers=headers)
    assert xlsx_res.status_code == 200
    assert "spreadsheetml" in xlsx_res.headers.get("content-type", "")
    assert len(xlsx_res.content) > 500

    # PDF
    pdf_res = client.get("/api/reports/pdf", headers=headers)
    assert pdf_res.status_code == 200
    assert "pdf" in pdf_res.headers.get("content-type", "")
    assert pdf_res.content.startswith(b"%PDF")


def test_html_pages_render(client):
    # Public transparency
    res_trans = client.get("/transparency")
    assert res_trans.status_code == 200
    assert "पारदर्शिता" in res_trans.text

    # Switch persona to admin and access department & predictive
    client.get("/switch-persona/admin")
    
    res_dept = client.get("/department")
    assert res_dept.status_code == 200
    assert "Department" in res_dept.text or "विभाग" in res_dept.text

    res_pred = client.get("/predictive")
    assert res_pred.status_code == 200
    assert "पूर्वानुमान" in res_pred.text

    # Switch persona to operator and access officer queue
    client.get("/switch-persona/operator")
    res_off = client.get("/officer")
    assert res_off.status_code == 200
    assert "अधिकारी" in res_off.text or "Officer" in res_off.text
