import pytest
import os
from playwright.sync_api import Page

@pytest.fixture
def frontend_url():
    # Allow override via env var, default to production URL
    return os.environ.get("FRONTEND_URL", "https://v-chess.com")

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--disable-web-security"]
    }

@pytest.fixture(autouse=True)

def set_default_timeout(page: Page):

    page.set_default_timeout(5000)

    yield
