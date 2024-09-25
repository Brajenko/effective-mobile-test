from faker import Faker


import pytest
from fastapi.testclient import TestClient
from backend.main import app

from core.config import settings


@pytest.fixture(scope="session", autouse=True)
def app():
    return app


@pytest.fixture(scope="session")
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def fake():
    return Faker()


@pytest.fixture(scope="session")
def products_url():
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.products}"


@pytest.fixture(scope="session")
def orders_url():
    return f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.orders}"
