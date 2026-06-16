import allure
import json
from pages.home_page import HomePage
from pathlib import Path
from playwright.sync_api import Page, expect
import pytest


# def test_forward_back_navigation(page: Page) -> None:
#     page.goto("https://example.com")
#     page.get_by_role("link", name="Products").click()
#     expect(page).to_have_url("/products")

#     page.go_back()
#     expect(page).to_have_url("https://example.com/")

#     page.go_forward()
#     expect(page).to_have_url("/products")
def load_users():
    data = json.loads(Path(__file__).parent.parent.parent.joinpath("data","users.json").read_text(encoding="utf-8"))
    return [(u["email"], u["password"], u["fname"], u["surname"]) for u in data]

@allure.feature("Account Creation")
@allure.story("User can navigate to account creation page and fill form")
@pytest.mark.parametrize("email,password,fname,surname", load_users())
def test_account_creation(page: Page, email: str, password: str, fname: str, surname: str) -> None:

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
        expect(home_page.account_link).to_be_visible(), "Account link should be visible in user menu"
    with allure.step("Click on account link and verify navigation"):
        home_page.account_link.click()
        expect(page).to_have_url("./register")
        page.wait_for_load_state("domcontentloaded")
        expect(page.get_by_role("heading", name="Create Account")).to_be_visible(), "Should navigate to account creation page"
    with allure.step("Enter registration details and submit form"):
        page.get_by_label("First Name").fill(fname)
        page.get_by_label("Last Name").fill(surname)
        page.get_by_label("Email").fill(email)
        page.locator("input[name='password']").fill(password)
        page.get_by_role("button", name="Create Account").click()
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("./")
        page.wait_for_load_state("domcontentloaded")
    with allure.step("Verify user is logged in after registration"):
        home_page.open_user_menu()
        expect(page.get_by_role("listitem", name="Welcome: "+fname)).to_be_visible(), "Account link should be visible in user menu after registration"
        expect(page.get_by_role("link", name="Account Overview")).to_be_visible(), "Account link should be visible in user menu after registration"
        expect(page.get_by_role("link", name="Logout")).not_to_be_visible(), "Logout link should not be visible in user menu after registration"


    


# def test_popup_dialog(page: Page) -> None:
#     """Handle JavaScript alert/confirm/prompt dialogs."""
#     page.goto("https://example.com")

#     # Auto-accept all dialogs
#     page.on("dialog", lambda dialog: dialog.accept())
#     page.get_by_role("button", name="Delete").click()

#     # Or inspect and handle
#     def handle_dialog(dialog):
#         assert dialog.message == "Are you sure you want to delete?"
#         dialog.accept()

#     page.on("dialog", handle_dialog)
#     page.get_by_role("button", name="Delete Item").click()


# def test_iframe_interaction(page: Page) -> None:
#     page.goto("https://example.com/embed")

#     # Get frame by URL pattern or name
#     frame = page.frame_locator("iframe[name='payment']")

#     # Interact inside the iframe
#     frame.get_by_label("Card number").fill("4111111111111111")
#     frame.get_by_label("Expiry").fill("12/26")
#     frame.get_by_role("button", name="Pay").click()


# def test_full_checkout_flow(page: Page) -> None:
#     """Multi-step scenario test."""
#     # Step 1: Browse
#     page.goto("https://shop.example.com")
#     page.get_by_role("link", name="Laptop Pro").click()
#     expect(page.get_by_role("heading")).to_contain_text("Laptop Pro")

#     # Step 2: Add to cart
#     page.get_by_role("button", name="Add to Cart").click()
#     expect(page.get_by_test_id("cart-count")).to_have_text("1")

#     # Step 3: Checkout
#     page.get_by_role("link", name="Cart").click()
#     page.get_by_role("button", name="Proceed to Checkout").click()
#     expect(page).to_have_url("/checkout")

#     # Step 4: Fill shipping
#     page.get_by_label("Full Name").fill("Alice Smith")
#     page.get_by_label("Address").fill("123 Main St")
#     page.get_by_role("button", name="Continue to Payment").click()

#     # Step 5: Confirm order page
#     expect(page).to_have_url("/checkout/payment")