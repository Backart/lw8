"""Tests for API endpoints."""

from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_task():
    """Test the task creation endpoint."""
    payload = {"title": "Test CI/CD", "user": "test@example.com"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Task created successfully"
