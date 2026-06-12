from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class DashboardPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.welcome_heading = page.get_by_role("heading", level=1)
        self.logout_button = page.get_by_role("button", name="Logout")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url("/dashboard")
        expect(self.welcome_heading).to_be_visible()
