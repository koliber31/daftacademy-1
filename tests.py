from fastapi.testclient import TestClient
from main import app


def test_categories():
    with TestClient(app) as client:
        response = client.get("/categories")
        assert response.status_code == 200


def test_customers():
    with TestClient(app) as client:
        response = client.get("/customers")
        assert response.status_code == 200


def test_category_add():
    with TestClient(app) as client:
        json = {"name": "test category"}
        response = client.post("/categories", json=json)
        assert response.status_code == 201
        assert response.json() == {"id": 30, "name": "test category"}


def test_category_put():
    with TestClient(app) as client:
        json = {"name": 'new changed'}
        response = client.put("/categories/30", json=json)
        assert response.status_code == 200
        assert response.json() == {"id": 30, "name": "changed"}


def test_category_put_wrong_id():
    with TestClient(app) as client:
        json = {"name": 'changed'}
        response = client.put("/categories/105", json=json)
        assert response.status_code == 404


def test_category_delete():
    with TestClient(app) as client:
        response = client.delete("/categories/30")
        assert response.status_code == 200
        assert response.json() == {"deleted": 1}
