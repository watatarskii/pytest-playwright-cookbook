from playwright.sync_api import Page
import pytest


def test_manual_screenshot(page: Page) -> None:
    page.goto("https://example.com")

    # Full page screenshot
    page.screenshot(path="test-results/full-page.png", full_page=True)

    # Clip to specific element
    element = page.get_by_role("main")
    element.screenshot(path="test-results/main-content.png")


def test_screenshot_on_assertion_failure(page: Page) -> None:
    """
    With --screenshot on-failure in pytest.ini, screenshots are auto-saved.
    This shows how to take a manual one at a specific step.
    """
    page.goto("https://example.com/cart")
    page.screenshot(path="test-results/before-submit.png")

    page.get_by_role("button", name="Submit").click()
    page.screenshot(path="test-results/after-submit.png")