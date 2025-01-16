import pytest
from application.api.main import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from logic.initial_container import init_container

from tests.fixtures import init_dummy_container


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[init_container] = init_dummy_container
    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
