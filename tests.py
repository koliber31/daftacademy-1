import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello world!'}


@pytest.mark.parametrize("name", ["Zenek", "Marek", "Alojzy Niezdąży"])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.text == f'"Hello {name}"'


def test_method_code_get():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {'method': 'GET'}


def test_method_code_put():
    response = client.put('/method')
    assert response.status_code == 200
    assert response.json() == {'method': 'PUT'}


def test_method_code_delete():
    response = client.delete('/method')
    assert response.status_code == 200
    assert response.json() == {'method': 'DELETE'}


def test_method_code_options():
    response = client.options('/method')
    assert response.status_code == 200
    assert response.json() == {'method': 'OPTIONS'}


def test_method_code_post():
    response = client.post("/method")
    assert response.status_code == 201
    assert response.json() == {'method': 'POST'}
