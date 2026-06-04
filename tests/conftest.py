from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def mock_table():
    with patch("app.main.table") as mocked:
        yield mocked


@pytest.fixture()
def client(mock_table):
    from app.main import app

    return TestClient(app)
