import pytest
import os

@pytest.fixture
def frontend_url():
    # Allow override via env var, default to local dev server
    return os.environ.get("FRONTEND_URL", "http://localhost:3000")

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--disable-web-security"]
    }

@pytest.fixture(autouse=True)
def setup_test_db():
    # Override root async fixture with a sync no-op for E2E
    pass