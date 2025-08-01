from collections.abc import Generator

from sqlmodel import Session, delete

import pytest
from fastapi.testclient import TestClient

from app.core.database import engine, init_db
from app.tests.api.utils import get_superuser_token_headers
from app.main import app
from app.models.user import User

# db session fixture
@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        session.exec(delete(User))
        session.commit()

# client module fixture
@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c

# token headers module fixture
@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture
def sample_user():
    return {
    "username": "john",
    "email": "john@gmail.com",
    "password": "super_strong12"
    }
