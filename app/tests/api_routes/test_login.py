from fastapi.testclient import TestClient

from app.core.config import get_settings


def test_login(client: TestClient) -> None:
    login_data = {
        "username": get_settings().superuser,
        "password": get_settings().superuser_password,
    }
    r = client.post("http://127.0.1:8000/api/auth/login/access_token", data=login_data)
    assert r.status_code == 200
    result = r.json()
    assert result["access_token"]
    assert result["token_type"]


def test_login_invalid_username(client: TestClient) -> None:
    login_data = {
        "username": "fake_username",
        "password": get_settings().superuser_password,
    }
    r = client.post("http://127.0.1:8000/api/auth/login/access_token", data=login_data)
    assert r.status_code == 401


def test_login_invalid_password(client: TestClient) -> None:
    login_data = {"username": get_settings().superuser, "password": "fake_password"}
    r = client.post("http://127.0.1:8000/api/auth/login/access_token", data=login_data)
    assert r.status_code == 401
