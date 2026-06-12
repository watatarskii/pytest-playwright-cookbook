from playwright.sync_api import Page, expect


def test_forward_back_navigation(page: Page) -> None:
    page.goto("https://example.com")
    page.get_by_role("link", name="Products").click()
    expect(page).to_have_url("/products")

    page.go_back()
    expect(page).to_have_url("https://example.com/")

    page.go_forward()
    expect(page).to_have_url("/products")


def test_new_tab_opens(page: Page, context) -> None:
    """
    Use 'context' fixture (BrowserContext) to capture new tabs.
    """
    page.goto("https://example.com")

    # Capture new page opened by click
    with context.expect_page() as new_page_info:
        page.get_by_role("link", name="Open in new tab").click()

    new_page = new_page_info.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_url("https://docs.example.com")
    new_page.close()


def test_popup_dialog(page: Page) -> None:
    """Handle JavaScript alert/confirm/prompt dialogs."""
    page.goto("https://example.com")

    # Auto-accept all dialogs
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Delete").click()

    # Or inspect and handle
    def handle_dialog(dialog):
        assert dialog.message == "Are you sure you want to delete?"
        dialog.accept()

    page.on("dialog", handle_dialog)
    page.get_by_role("button", name="Delete Item").click()


def test_iframe_interaction(page: Page) -> None:
    page.goto("https://example.com/embed")

    # Get frame by URL pattern or name
    frame = page.frame_locator("iframe[name='payment']")

    # Interact inside the iframe
    frame.get_by_label("Card number").fill("4111111111111111")
    frame.get_by_label("Expiry").fill("12/26")
    frame.get_by_role("button", name="Pay").click()


def test_full_checkout_flow(page: Page) -> None:
    """Multi-step scenario test."""
    # Step 1: Browse
    page.goto("https://shop.example.com")
    page.get_by_role("link", name="Laptop Pro").click()
    expect(page.get_by_role("heading")).to_contain_text("Laptop Pro")

    # Step 2: Add to cart
    page.get_by_role("button", name="Add to Cart").click()
    expect(page.get_by_test_id("cart-count")).to_have_text("1")

    # Step 3: Checkout
    page.get_by_role("link", name="Cart").click()
    page.get_by_role("button", name="Proceed to Checkout").click()
    expect(page).to_have_url("/checkout")

    # Step 4: Fill shipping
    page.get_by_label("Full Name").fill("Alice Smith")
    page.get_by_label("Address").fill("123 Main St")
    page.get_by_role("button", name="Continue to Payment").click()

    # Step 5: Confirm order page
    expect(page).to_have_url("/checkout/payment")