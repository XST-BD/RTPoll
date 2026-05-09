import pytest
import requests

# This fixture will be available to all your test files
@pytest.fixture(scope="session")
def api_base_url():
    return "http://127.0.0.1:8000"


_poll_id: int

@pytest.fixture(scope="session")
def set_poll_id(poll_id: int):
    _poll_id = poll_id

@pytest.fixture(scope="session")
def shared_data():
    return {
        "access_token": None,
        "poll_id": None,
        "user_id": None
    }

@pytest.fixture(scope='session')
def session():
    with requests.Session() as s:
        yield s