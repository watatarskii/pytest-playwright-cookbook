from concurrent.futures import wait

import allure
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import Browser, BrowserContext
from pages.home_page import HomePage

@allure.feature("Home Page")
@allure.story("Visibility of main elements")
def test_homepage_elements(page: Page) -> None:
    home_page = HomePage(page)
    with allure.step("Open home page"):
        home_page.open()
    with allure.step("Verify main components are visible"):
        assert home_page.header.is_visible(), "Header should be visible on home page"
        assert home_page.main_content.is_visible(), "Main content should be visible on home page"
        assert home_page.footer.is_visible(), "Footer should be visible on home page"
        expect(home_page.cart_link).to_be_visible(), "Cart link should be visible on home page"
    with allure.step("Open user menu and verify login link is visible"):
        home_page.open_user_menu()
        expect(home_page.login_link).to_be_visible(), "Login link should be visible in user menu"