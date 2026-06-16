import pytest
from playwright.sync_api import Page, expect


# ---- Basic parameterization ----

@pytest.mark.parametrize("search_term,expected_count", [
    ("Python", 5),
    ("JavaScript", 8),
    ("Rust", 2),
])
def test_search_results(page: Page, search_term: str, expected_count: int) -> None:
    page.goto("https://example.com/search")
    page.get_by_role("searchbox").fill(search_term)
    page.get_by_role("searchbox").press("Enter")

    results = page.get_by_role("listitem")
    expect(results).to_have_count(expected_count)


# ---- Testing invalid login scenarios ----

INVALID_CREDENTIALS = [
    ("", "password123", "Email is required"),
    ("not-an-email", "password123", "Invalid email format"),
    ("user@example.com", "", "Password is required"),
    ("user@example.com", "wrong", "Invalid credentials"),
]

@pytest.mark.parametrize("email,password,expected_error", INVALID_CREDENTIALS)
def test_login_validation(page: Page, email: str, password: str, expected_error: str) -> None:
    page.goto("/login")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Sign in").click()

    expect(page.get_by_role("alert")).to_contain_text(expected_error)


# ---- Load test data from JSON ----

import json
from pathlib import Path


def load_users():
    data = json.loads(Path("..\\pytest-playwright-cookbook\\WEB_UI\\data\\users.json").read_text())
    return [(u["email"], u["password"], u["name"], u["surname"]) for u in data]


@pytest.mark.parametrize("email,password,expected_url", load_users())
def test_user_roles(page: Page, email: str, password: str, expected_url: str) -> None:
    page.goto("/login")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Sign in").click()

    expect(page).to_have_url(expected_url)