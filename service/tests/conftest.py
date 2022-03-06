import os
import json

import pytest
from sqlalchemy import create_engine, MetaData
from async_asgi_testclient import TestClient

from app import app
from app.db import Tasks


test_engine = create_engine(os.environ["DATABASE_URI"])
test_meta = MetaData()


@pytest.fixture()
async def cli():
    async with TestClient(app) as client:
        yield client


@pytest.yield_fixture(scope="session")
def db_data():
    create_tables()
    load_from_fixtures()
    yield
    drop_tables()


FIXTURED = (Tasks,)
FIXTURES_PATH = "tests/json_fixtures/"


def create_tables():
    test_meta.create_all(bind=test_engine, tables=[each.table for each in FIXTURED])


def drop_tables():
    test_meta.drop_all(bind=test_engine, tables=[each.table for each in FIXTURED])


def load_from_fixtures():
    """
    loads tests json-fixture to database
    each json-fixture must be named as lowercase-classname.json
    example: Tasks tasks.json
    """
    with test_engine.connect() as connection:
        for each in FIXTURED:
            with open(f"{FIXTURES_PATH}/{each.__qualname__.lower()}.json") as f:
                json_data = json.load(f)
                for record in json_data:
                    connection.execute(each.table.insert(), record)
