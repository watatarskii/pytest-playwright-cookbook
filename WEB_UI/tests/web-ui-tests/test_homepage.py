import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import Browser, BrowserContext
from pages.home_page import HomePage


def test_homepage_elements(page: Page) -> None:
    home_page = HomePage(page)
    home_page.open()
    assert home_page.header.is_visible(), "Header should be visible on home page"
    assert home_page.main_content.is_visible(), "Main content should be visible on home page"
    assert home_page.footer.is_visible(), "Footer should be visible on home page"
    assert home_page.login_link.is_visible(), "Login link should be visible on home page"
    assert home_page.cart_link.is_visible(), "Cart link should be visible on home page"