import json
from pathlib import Path
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright
from pages.login_page import LoginPage


# ---- Register custom CLI option ----
def pytest_addoption(parser):
    parser.addoption(
        "--locale",
        action="store",
        default="en-US",
        help="Locale for browser context (e.g., en-US, de-DE, ru-RU)"
    )


# ---- Browser context with custom settings ----

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, request):
    """Override default browser context settings for ALL tests."""
    locale = request.config.getoption("--locale")
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": locale,
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
        "name": "Test",
        "surname": "User",
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
    
AUTH_FILE = Path("test-results/auth.json")


@pytest.fixture(scope="session")
def authenticated_context(browser: Browser) -> BrowserContext:
    """
    Log in ONCE per test session. Save cookies/localStorage to disk.
    All tests using this fixture skip the login step.
    """
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://example.com/login")
    page.get_by_label("Email").fill("testuser@example.com")
    page.get_by_label("Password").fill("password123")
    page.get_by_role("button", name="Sign in").click()

    # Wait until actually logged in
    page.wait_for_url("**/dashboard")

    # Save state (cookies + localStorage) to disk
    context.storage_state(path=str(AUTH_FILE))
    page.close()

    yield context
    context.close()


@pytest.fixture
def auth_page(browser: Browser) -> Page:
    """
    Create a new context from saved auth state for each test.
    Each test gets an isolated session but is already logged in.
    """
    context = browser.new_context(storage_state=str(AUTH_FILE))
    page = context.new_page()
    yield page
    context.close()
    
@pytest.fixture(scope="session")
def authenticated_context_via_api(playwright: Playwright, browser: Browser) -> BrowserContext:
    """Log in via API call instead of UI"""
    request = playwright.request.new_context(base_url="https://api.example.com")
    response = request.post("/auth/login", data={
        "email": "testuser@example.com",
        "password": "password123"
    })
    token = response.json()["access_token"]

    context = browser.new_context(extra_http_headers={
        "Authorization": f"Bearer {token}"
    })
    request.dispose()
    yield context
    context.close()
    
@pytest.fixture
def browser_context_args(browser_context_args, request):
    locale = request.config.getoption("--locale", default="en-US")
    return {
        **browser_context_args,
        "locale": locale,
    }