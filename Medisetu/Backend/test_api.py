import io
import json
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200

    data = res.json()
    assert data["status"] == "ok"
    assert data["service"] == "MediSetu API"

def test_blood_text_valid(client):
    res = client.post(
        "/api/blood/analyse",
        data={
            "text": "Hemoglobin: 12.5 g/dL\nWBC: 7500 /cumm",
            "gender": "Male",
            "language": "English"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert "engine_results" in data
    assert "report_text" in data
    assert isinstance(data.get("report_text"), str)
    assert isinstance(data.get("llm_response"), str)
    assert isinstance(data.get("engine_results"), dict)


def test_blood_no_input(client):
    res = client.post("/api/blood/analyse")
    assert res.status_code == 400
    assert "No input provided" in res.json()["detail"]


def test_blood_empty_text(client):
    res = client.post("/api/blood/analyse", data={"text": "   "})
    assert res.status_code == 400

def test_radiology_text_valid(client):
    res = client.post(
        "/api/radiology/analyse",
        data={"text": "Normal chest X-ray. No abnormality."}
    )
    assert res.status_code == 200
    data = res.json()
    assert "engine_results" in data
    assert "report_text" in data
    assert isinstance(data.get("report_text"), str)
    assert isinstance(data.get("llm_response"), str)
    assert isinstance(data.get("engine_results"), dict)

def test_prescription_text_valid(client):
    """Backend supports TEXT → must pass"""
    res = client.post(
        "/api/prescription/analyse",
        data={"text": "Tab. Paracetamol 500mg 1-0-1"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "engine_results" in data
    assert "report_text" in data
    assert isinstance(data.get("report_text"), str)
    assert isinstance(data.get("llm_response"), str)
    assert isinstance(data.get("engine_results"), dict)


def test_prescription_invalid_file(client):
    res = client.post(
        "/api/prescription/analyse",
        files={"file": ("test.txt", io.BytesIO(b"abc"), "text/plain")}
    )
    assert res.status_code in (400, 500)
    if res.status_code == 400:
        assert "Only image files are supported" in res.json()["detail"]

def test_skin_text_valid(client):
    res = client.post(
        "/api/skin/analyse",
        data={"text": "Red itchy rash for 5 days"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "engine_results" in data
    assert data["mode"] == "text"
    assert isinstance(data.get("llm_response"), str)
    assert isinstance(data.get("engine_results"), dict)

def test_blood_pdf_upload(client):
    fake_pdf = io.BytesIO(b"%PDF-1.4 fake")
    res = client.post(
        "/api/blood/analyse",
        files={"file": ("report.pdf", fake_pdf, "application/pdf")}
    )
    assert res.status_code in (200, 400)

def test_blood_image_upload(client):
    fake_image = io.BytesIO(
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
    )
    res = client.post(
        "/api/blood/analyse",
        files={"file": ("img.png", fake_image, "image/png")}
    )
    assert res.status_code in (200, 400)


def test_invalid_file_type_blood(client):
    res = client.post(
        "/api/blood/analyse",
        files={"file": ("bad.txt", io.BytesIO(b"abc"), "text/plain")}
    )
    assert res.status_code in (400,429)

def test_chat_valid(client):
    res = client.post(
        "/api/chat",
        data={
            "report_text": "Hb: 10",
            "question": "Is it normal?",
            "chat_history": json.dumps([])
        }
    )
    assert res.status_code == 200
    assert isinstance(res.json().get("reply"), str)


def test_chat_invalid_history(client):
    res = client.post(
        "/api/chat",
        data={
            "report_text": "Hb: 10",
            "question": "Explain",
            "chat_history": "invalid_json"
        }
    )
    assert res.status_code == 200

def test_feedback_endpoint(client):
    res = client.post(
        "/api/feedback",
        data={
            "report_type": "blood",
            "feedback_type": "positive",
            "feedback_text": "Very helpful"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"

def test_rate_limiting(client):
    hit_429 = False
    for _ in range(12):
        res = client.post(
            "/api/blood/analyse",
            data={"text": "rate test"}
        )
        if res.status_code == 429:
            hit_429 = True
            break
    assert hit_429, "Rate limiting did not trigger"