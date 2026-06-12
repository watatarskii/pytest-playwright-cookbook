import json
from playwright.sync_api import Page, expect, Route


def test_mock_api_response(page: Page) -> None:
    """Replace a real API call with a fake response."""

    def mock_users(route: Route) -> None:
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([
                {"id": 1, "name": "Alice Mock", "email": "alice@mock.com"},
                {"id": 2, "name": "Bob Mock", "email": "bob@mock.com"},
            ])
        )

    page.route("**/api/users", mock_users)
    page.goto("https://example.com/users")

    # The UI should render our mocked data
    expect(page.get_by_text("Alice Mock")).to_be_visible()
    expect(page.get_by_text("Bob Mock")).to_be_visible()


def test_mock_api_error(page: Page) -> None:
    """Test how the UI handles a server error."""

    page.route("**/api/data", lambda route: route.fulfill(
        status=500,
        body="Internal Server Error"
    ))

    page.goto("https://example.com/dashboard")

    expect(page.get_by_role("alert")).to_contain_text("Something went wrong")


def test_abort_request(page: Page) -> None:
    """Block specific requests (e.g., analytics, ads)."""
    page.route("**/*.{png,jpg,jpeg,webp}", lambda route: route.abort())

    page.goto("https://example.com")
    # Page loads without images (faster test execution)


def test_intercept_and_modify(page: Page) -> None:
    """Intercept request, modify it, then continue."""

    def add_auth_header(route: Route) -> None:
        headers = {**route.request.headers, "Authorization": "Bearer fake_token"}
        route.continue_(headers=headers)

    page.route("**/api/**", add_auth_header)
    page.goto("https://example.com/protected")


def test_capture_request(page: Page) -> None:
    """Verify the app sends the right request payload."""
    captured_body = {}

    def capture(route: Route) -> None:
        captured_body.update(json.loads(route.request.post_data or "{}"))
        route.continue_()

    page.route("**/api/order", capture)

    page.goto("https://example.com/checkout")
    page.get_by_role("button", name="Place Order").click()

    assert captured_body.get("currency") == "EUR"
    assert captured_body.get("items") is not None