from fastapi.testclient import TestClient

from app.main import app

test_client = TestClient(app)


def test_health():
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the ProComp API!"}
