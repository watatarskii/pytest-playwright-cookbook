import pytest
from playwright.sync_api import Page, expect

def test_locator_strategies(page: Page) -> None:
    page.goto("https://demo.playwright.dev/todomvc")

    # --- PREFERRED: Semantic locators (accessible, resilient) ---

    # By role + name (matches ARIA role and accessible name)
    new_todo = page.get_by_role("textbox", name="What needs to be done?")
    new_todo.fill("Buy groceries")
    new_todo.press("Enter")

    # By label (matches <label> text)
    # page.get_by_label("Email address").fill("user@test.com")

    # By placeholder text
    page.get_by_placeholder("What needs to be done?").fill("Walk the dog")
    page.get_by_placeholder("What needs to be done?").press("Enter")

    # By visible text content
    page.get_by_text("Buy groceries").click()

    # By test ID (requires data-testid attribute in HTML — ask devs to add these!)
    # page.get_by_test_id("submit-button").click()

    # --- ACCEPTABLE: CSS and XPath (fragile but sometimes necessary) ---

    # CSS selector
    page.locator(".new-todo").fill("Clean the house")
    page.locator(".new-todo").press("Enter")

    # XPath (last resort — brittle)
    # page.locator("//input[@class='new-todo']").fill("...")

    # Nth element in a list
    items = page.get_by_role("listitem")
    first_item = items.nth(0)
    expect(first_item).to_contain_text("Buy groceries")

    # Filter locators
    done_items = page.get_by_role("listitem").filter(has_text="Buy groceries")
    expect(done_items).to_have_count(1)

    # Assert total count
    expect(page.get_by_test_id("todo-item")).to_have_count(3) # Assuming we added 3 items in this test, can be found only by "todo-item" test id, otherwise will take buttons as list items as well


def test_element_states(page: Page) -> None:
    """Test checking element visibility, enabled state, values."""
    page.goto("https://demo.playwright.dev/todomvc")

    input_box = page.get_by_role("textbox")

    expect(input_box).to_be_visible()
    expect(input_box).to_be_enabled()
    expect(input_box).to_be_empty()

    input_box.fill("Test item")
    expect(input_box).to_have_value("Test item")