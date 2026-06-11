from playwright.sync_api import Page


class BasePage:
    """All page objects inherit from this."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()
