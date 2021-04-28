import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello_view():
    response = client.get("/hello")
    assert response.status_code == 200


def test_login_session_ok():
    response = client.post('/login_session?user=4dm1n&password=NotSoSecurePa$$')
    assert response.status_code == 200
    # assert response.set_cookie ==


def test_login_session_nok():
    response = client.post('/login_session?user=4dm1n&password=wrong')
    assert response.status_code == 401


def test_login_token_ok():
    response = client.post('/login_session?user=4dm1n&password=NotSoSecurePa$$')
    assert response.status_code == 200
    assert response.json() == {"token": 'c8730304beb5f0e94434af0869469a86069a2aa7a824e95b7e8cee9ba14bbac6'}
