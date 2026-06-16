from playwright.sync_api import Page, expect
import re


def test_wait_for_element(page: Page) -> None:
    page.goto("https://example.com/slow-page")

    # expect() auto-waits up to the timeout
    expect(page.get_by_role("heading")).to_be_visible()

    # visible, stable, enabled, and not obscured before acting
    page.get_by_role("button", name="Load Data").click()


def test_wait_for_network(page: Page) -> None:
    page.goto("https://example.com")

    # Wait for all network requests to finish before clicking
    with page.expect_response("**/api/data") as response_info:
        page.get_by_role("button", name="Refresh").click()

    response = response_info.value
    assert response.status == 200


def test_wait_for_navigation(page: Page) -> None:
    page.goto("https://example.com")

    # Wait for URL change caused by a click
    with page.expect_navigation():
        page.get_by_role("link", name="About").click()

    expect(page).to_have_url(re.compile(r".*/about"))


def test_wait_for_dom_change(page: Page) -> None:
    page.goto("https://example.com/async")

    page.get_by_role("button", name="Submit").click()

    # Wait for a specific element to appear
    success_toast = page.get_by_role("status")
    expect(success_toast).to_be_visible(timeout=10_000)  # override timeout to 10s


def test_custom_polling(page: Page) -> None:
    page.goto("https://example.com/job")

    page.get_by_role("button", name="Start Job").click()

    # Wait for text to change (e.g. progress indicator)
    expect(page.get_by_test_id("job-status")).to_have_text("Completed", timeout=30_000)