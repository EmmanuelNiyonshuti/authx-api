from starlette.testclient import TestClient

from app.core.config import get_settings
from app.tests.api.utils import BASE_URL

LOGIN_URL = f"{BASE_URL}/auth/login/access_token"

def test_login_success(client: TestClient) -> None:
    login_data = {
        "username": get_settings().superuser_username,
        "password": get_settings().superuser_password,
    }
    r = client.post(LOGIN_URL, data=login_data) # form data
    assert r.status_code == 200
    result = r.json()
    assert result["access_token"]
    assert result["token_type"]

def test_login_failure_invalid_credentials(client: TestClient) -> None:
    login_data = {
        "username": get_settings().superuser_username,
        "password": "wrongpassword",
    }
    r = client.post(LOGIN_URL, data=login_data)
    assert r.status_code == 401
    assert r.json() == {"detail": "Incorrect username or password"}
