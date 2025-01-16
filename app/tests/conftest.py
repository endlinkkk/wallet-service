import pytest
from punq import Container

from tests.fixtures import init_dummy_container


@pytest.fixture(scope="session")
def container() -> Container:
    return init_dummy_container()
