import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage

def test_dashboard_shows_username(logged_in_page: Page, test_user: dict) -> None:
    """This test gets a pre-authenticated page automatically."""
    heading = logged_in_page.get_by_role("heading")
    expect(heading).to_contain_text(test_user["name"])