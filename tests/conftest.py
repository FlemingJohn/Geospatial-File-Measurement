import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setenv("GEOSPATIAL_STORAGE_DIRECTORY", str(tmp_path / "storage"))
    return TestClient(create_app())
