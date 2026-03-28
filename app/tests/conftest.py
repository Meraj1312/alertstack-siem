import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db


@pytest.fixture
def client():
    init_db()

    with TestClient(app) as client:
        yield client