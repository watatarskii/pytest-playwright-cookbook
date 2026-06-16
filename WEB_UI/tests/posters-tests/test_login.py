import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import Browser, BrowserContext
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_successful_login(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.open()
    assert login_page.email_input.is_visible(), "Email input should be visible on login page"
    assert login_page.password_input.is_visible(), "Password input should be visible on login page"
    login_page.login("user@example.com", "correct_password")

    dashboard = DashboardPage(page)
    dashboard.expect_loaded()


def test_wrong_password_shows_error(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("user@example.com", "wrong_password")

    login_page.expect_error("Invalid credentials")


def test_empty_email_shows_validation(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("", "any_password")

    login_page.expect_error("Email is required")