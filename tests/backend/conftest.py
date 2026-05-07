import pytest
import requests

# This fixture will be available to all your test files
@pytest.fixture(scope="session")
def api_base_url():
    return "http://localhost:8000"

@pytest.fixture
def session():
    """Provides a clean requests session for each test."""
    with requests.Session() as s:
        yield s