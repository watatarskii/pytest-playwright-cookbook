import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from pages.login_page import LoginPage


# ---- Browser context with custom settings ----

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default browser context settings for ALL tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
        "timezone_id": "Europe/Berlin",
        "ignore_https_errors": True,   # useful for local dev with self-signed certs
    }


# ---- Authenticated page fixture ----

@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """
    Provides a Page that is already logged in.
    Tests that need auth use this instead of 'page'.
    """
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("testuser@example.com", "password123")
    return page


# ---- Reusable data fixtures ----

@pytest.fixture
def test_user():
    return {
        "email": "testuser@example.com",
        "password": "password123",
        "name": "Test User",
    }


@pytest.fixture
def admin_user():
    return {
        "email": "admin@example.com",
        "password": "adminpass",
        "name": "Admin",
    }


# ---- API client fixture (for test data setup/teardown) ----

@pytest.fixture
def api_request_context(playwright):
    """
    Use Playwright's API client for setup/teardown without browser overhead.
    """
    request_context = playwright.request.new_context(
        base_url="https://api.example.com",
        extra_http_headers={"Authorization": "Bearer test_token"}
    )
    yield request_context
    request_context.dispose()