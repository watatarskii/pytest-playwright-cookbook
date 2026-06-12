from playwright.sync_api import Page, expect


def test_dashboard_loads(auth_page: Page) -> None:
    """Starts already logged in — no login steps needed."""
    auth_page.goto("/dashboard")
    expect(auth_page.get_by_role("heading", name="Dashboard")).to_be_visible()


def test_user_profile(auth_page: Page) -> None:
    auth_page.goto("/profile")
    expect(auth_page.get_by_label("Email")).to_have_value("testuser@example.com")