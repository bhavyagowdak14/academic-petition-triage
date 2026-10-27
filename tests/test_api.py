from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_submit_petition():
    payload = {
        "student_id": "TEST001",
        "petition_type": "Attendance Condonation",
        "semester": 3,
        "reason": "Medical emergency caused attendance shortage.",
        "attendance_percentage": 78.5,
        "supporting_evidence": "medical_certificate.pdf",
    }

    response = client.post("/petitions/submit", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "submitted"
    assert result["final_decision"] == "pending_human_review"


def test_invalid_attendance_rejected():
    payload = {
        "student_id": "TEST002",
        "petition_type": "Attendance Condonation",
        "semester": 3,
        "reason": "Medical emergency caused attendance shortage.",
        "attendance_percentage": 120,
        "supporting_evidence": None,
    }

    response = client.post("/petitions/submit", json=payload)

    assert response.status_code == 422