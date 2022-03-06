import pytest
from async_asgi_testclient import TestClient

from app import app


@pytest.fixture()
async def cli():
    async with TestClient(app) as client:
        yield client
