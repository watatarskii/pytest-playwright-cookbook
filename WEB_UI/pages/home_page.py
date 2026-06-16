from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "/home"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header = page.locator("header")
        self.main_content = page.locator("main")
        self.footer = page.locator("footer")
        self.user_menu_icon = page.locator("#user")
        self.user_menu_opened = page.locator("#user-menu")
        self.cart_link = page.locator("#mini-cart")

    def open(self) -> "HomePage":
        self.page.goto(self.URL)
        return self

    def open_user_menu(self) -> "HomePage":
        self.user_menu_icon.click()
        self.user_menu_opened.wait_for(state="visible")
        self.login_link = self.user_menu_opened.get_by_role("link", name="Sign in")
        self.account_link = self.user_menu_opened.get_by_role("link", name="Create account") or self.user_menu_opened.get_by_role("link", name="My account")
        return self
    
    