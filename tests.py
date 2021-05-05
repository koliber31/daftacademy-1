from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_categories():
    response = client.get("/categories")
    assert response.status_code == 200


def test_customers():
    response = client.get("/customers")
    assert response.status_code == 200