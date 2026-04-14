import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint_mock():
    # Ensure settings.LLM_PROVIDER is 'mock' for this test
    payload = {"prompt": "Hello, how are you?", "parameters": {}}
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

def test_metrics_endpoint():
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200

def test_drift_endpoint():
    response = client.get("/api/v1/drift")
    assert response.status_code == 200

def test_performance_summary():
    response = client.get("/api/v1/performance/summary")
    assert response.status_code == 200
