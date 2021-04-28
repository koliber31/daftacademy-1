import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello_view():
    response = client.get("/hello")
    assert response.status_code == 200
