import pytest
from playwright.sync_api import Page, expect, BrowserContext


# ---- Using built-in device emulation ----

@pytest.fixture
def mobile_page(browser):
    """Emulate an iPhone 14 Pro."""
    from playwright.sync_api import sync_playwright
    import playwright._impl._api_types as types

    context = browser.new_context(**{
        "viewport": {"width": 390, "height": 844},
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
        "is_mobile": True,
        "has_touch": True,
        "device_scale_factor": 3,
    })
    page = context.new_page()
    yield page
    context.close()


def test_hamburger_menu(mobile_page: Page) -> None:
    mobile_page.goto("https://example.com")

    # Desktop nav should be hidden
    expect(mobile_page.get_by_role("navigation")).to_be_hidden()

    # Hamburger button should be visible
    hamburger = mobile_page.get_by_role("button", name="Menu")
    expect(hamburger).to_be_visible()
    hamburger.click()

    # Nav should now be visible
    expect(mobile_page.get_by_role("navigation")).to_be_visible()


def test_touch_swipe(mobile_page: Page) -> None:
    mobile_page.goto("https://example.com/gallery")

    carousel = mobile_page.get_by_test_id("carousel")
    box = carousel.bounding_box()

    # Simulate swipe left
    mobile_page.touchscreen.tap(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    mobile_page.mouse.move(
        box["x"] + box["width"] * 0.8,
        box["y"] + box["height"] / 2
    )
    mobile_page.mouse.move(
        box["x"] + box["width"] * 0.2,
        box["y"] + box["height"] / 2
    )


def test_responsive_breakpoints(page: Page) -> None:
    """Test layout at different viewport widths."""
    page.goto("https://example.com")

    viewports = [
        (375, "mobile"),
        (768, "tablet"),
        (1280, "desktop"),
    ]

    for width, label in viewports:
        page.set_viewport_size({"width": width, "height": 900})
        page.screenshot(path=f"test-results/layout-{label}.png")
        # Assert layout-specific elements