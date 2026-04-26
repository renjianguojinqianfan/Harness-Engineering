"""Tests for main.py."""

from fastapi.testclient import TestClient

from {package_name}.main import app

client = TestClient(app)


def test_read_root() -> None:
    """GET / should return greeting."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_health_check() -> None:
    """GET /health should return ok status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
