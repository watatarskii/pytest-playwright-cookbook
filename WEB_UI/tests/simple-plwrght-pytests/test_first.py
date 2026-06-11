import pytest
from playwright.sync_api import Page, expect


def test_page_title(page: Page) -> None:
    """
    The 'page' fixture is provided by pytest-playwright automatically.
    It gives you a fresh browser page for each test.
    """
    page.goto("https://playwright.dev")

    # expect() is auto-retrying — it keeps checking until timeout
    expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")


def test_heading_is_visible(page: Page) -> None:
    page.goto("https://playwright.dev")

    heading = page.get_by_role("heading", name="Playwright enables reliable")
    expect(heading).to_be_visible()


def test_get_started_link_works(page: Page) -> None:
    page.goto("https://playwright.dev")

    # Click a link and verify navigation
    page.get_by_role("link", name="Get started").click()

    expect(page).to_have_url("https://playwright.dev/docs/intro")