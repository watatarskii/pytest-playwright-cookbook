from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "/home"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Define locators as attributes — easy to update in one place
        self.header = page.locator("header")
        self.main_content = page.locator("main")
        self.footer = page.locator("footer")
        self.user_menu = page.locator("#user")
        self.login_link = self.user_menu.get_by_role("button", name="Login")
        self.cart_link = page.locator("#mini-cart")
        

    def open(self) -> "HomePage":
        self.page.goto(self.URL)
        return self