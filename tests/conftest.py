import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Fixture untuk membuat test client FastAPI.
    Digunakan oleh semua test API.
    """
    return TestClient(app)