from starlette.testclient import TestClient

from app.tests.api.utils import BASE_URL

REGISTER_URL = f"{BASE_URL}/auth/register"

def test_register_user(client: TestClient, sample_user) -> None:
    r = client.post(REGISTER_URL, json=sample_user)
    assert r.status_code == 201
    r = client.post(REGISTER_URL, json=sample_user)
    assert r.status_code == 400
    assert r.json() == {"detail": "User already exists"}
