from pathlib import Path
from playwright.sync_api import Page, expect


def test_text_inputs(page: Page) -> None:
    page.goto("https://example.com/signup")

    # Standard text input
    page.get_by_label("First Name").fill("Alice")

    # Clear and retype
    page.get_by_label("Last Name").clear()
    page.get_by_label("Last Name").fill("Smith")

    # Type character by character (useful for autocomplete fields)
    page.get_by_label("City").type("Ber", delay=50)
    page.get_by_role("option", name="Berlin").click()

    # Press keyboard shortcuts
    page.get_by_label("First Name").press("Control+a")
    page.get_by_label("First Name").press("Backspace")


def test_select_dropdown(page: Page) -> None:
    page.goto("https://example.com/form")

    # Select by visible label
    page.get_by_label("Country").select_option(label="Germany")

    # Select by value attribute
    page.get_by_label("Language").select_option(value="de")

    # Select multiple options
    page.get_by_label("Interests").select_option(["sports", "music", "tech"])

    expect(page.get_by_label("Country")).to_have_value("DE")


def test_checkboxes_and_radio(page: Page) -> None:
    page.goto("https://example.com/preferences")

    # Checkbox — check / uncheck
    page.get_by_label("Subscribe to newsletter").check()
    expect(page.get_by_label("Subscribe to newsletter")).to_be_checked()

    page.get_by_label("Subscribe to newsletter").uncheck()
    expect(page.get_by_label("Subscribe to newsletter")).not_to_be_checked()

    # Radio button
    page.get_by_label("Monthly").check()
    expect(page.get_by_label("Monthly")).to_be_checked()
    expect(page.get_by_label("Yearly")).not_to_be_checked()


def test_file_upload(page: Page) -> None:
    page.goto("https://example.com/upload")

    # Single file upload
    upload_input = page.get_by_label("Upload document")
    upload_input.set_input_files("data/sample.pdf")

    # Multiple files
    upload_input.set_input_files(["data/file1.pdf", "data/file2.pdf"])

    # File upload via dialog (click triggers native dialog)
    with page.expect_file_chooser() as fc_info:
        page.get_by_role("button", name="Browse").click()
    file_chooser = fc_info.value
    file_chooser.set_files("data/sample.pdf")

    expect(page.get_by_text("sample.pdf")).to_be_visible()


def test_date_picker(page: Page) -> None:
    page.goto("https://example.com/booking")

    # For simple <input type="date">
    page.get_by_label("Check-in date").fill("2025-09-15")

    # For custom date picker widgets, you may need to click through
    page.get_by_test_id("date-picker").click()
    page.get_by_role("gridcell", name="15").click()