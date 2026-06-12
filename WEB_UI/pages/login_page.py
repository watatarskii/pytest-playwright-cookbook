from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Define locators as attributes — easy to update in one place
        self.email_input = page.get_by_test_id("email")
        self.password_input = page.get_by_test_id("password")
        self.submit_button = page.get_by_role("button", name="Anmelden")

    def open(self) -> "LoginPage":
        self.page.goto(self.URL)
        return self

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def expect_error(self, text: str) -> None:
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_contain_text(text)