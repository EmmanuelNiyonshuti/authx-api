import random
import string

from fastapi.testclient import TestClient

from app.core.config import get_settings

BASE_URL = get_settings().api_url

def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": get_settings().superuser_username,
        "password": get_settings().superuser_password,
    }
    r = client.post(f"{BASE_URL}/auth/login/access_token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
