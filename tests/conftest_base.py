from pytest import fixture
from fastapi.testclient import TestClient

from app.main import create_app


@fixture(scope="session")
def app():
    return create_app()


@fixture(scope="session")
def client(app):
    return TestClient(app)
