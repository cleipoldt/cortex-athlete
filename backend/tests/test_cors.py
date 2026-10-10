from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_allowed_origin_receives_cors_header():
    response = client.get("/health", headers={"Origin": "http://localhost:5173"})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_unknown_origin_receives_no_cors_header():
    response = client.get("/health", headers={"Origin": "https://evil.example"})

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers