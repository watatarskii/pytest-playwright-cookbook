import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_successful_login(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.open()
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