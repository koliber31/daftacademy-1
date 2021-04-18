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


def test_auth_sha512_ok():
    response = client.get("/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61" +
                          "bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == 204


def test_auth_sha512_nok():
    response = client.get("/auth?password=haslo" +
                          "&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900" +
                          "e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response.status_code == 401


def test_auth_sha512_no_password_hash():
    response = client.get("/auth?password=haslo")
    assert response.status_code == 401


def test_auth_sha512_no_password():
    response = client.get("/auth?password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105" +
                          "e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == 401


def test_register_view():
    response = client.post("/register?name=Lukasz&surname=Szymanski")
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'name': 'Lukasz',
        'surname': 'Szymanski',
        'register_date': '2021-04-18',
        'vaccination_date': '2021-05-03'
    }
