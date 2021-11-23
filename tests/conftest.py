from typing import AsyncGenerator

import pytest
from app.db import database
from app.main import app
from starlette.testclient import TestClient


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
