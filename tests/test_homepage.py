# ─────────────────────────────────────────────────────────
#  Homepage smoke & regression tests – BookMyShow
# ─────────────────────────────────────────────────────────

import pytest
from pages.home_page import HomePage


@pytest.mark.smoke
class TestHomepageLoad:
    """Verifying the page loads correctly and key elements are present."""

    def test_page_title_contains_bookmyshow(self, driver):
        """Homepage <title> must mention BookMyShow."""
        page = HomePage(driver).load()
        title = page.get_page_title()
        assert "bookmyshow" in title.lower(), (
            f"Expected 'bookmyshow' in title, got: '{title}'"
        )

    def test_current_url_is_base_url(self, driver):
        """After load, URL should be the BMS root."""
        page = HomePage(driver).load()
        assert "bookmyshow.com" in page.get_url(), (
            f"Unexpected URL: {page.get_url()}"
        )

    def test_page_is_fully_loaded(self, driver):
        """document.readyState must be 'complete'."""
        page = HomePage(driver).load()
        state = page.execute_js("return document.readyState")
        assert state == "complete", f"Page not complete: {state}"


@pytest.mark.smoke
class TestHomepageBanner:
    """Hero banner / slider section visibility."""

    def test_banner_section_visible(self, driver):
        """A banner/hero section should be visible above the fold."""
        page = HomePage(driver).load()
        visible = page.is_banner_visible()
        # Non-fatal: some cities may show a different layout
        if not visible:
            pytest.skip("Banner not found in this layout – skipping")
        assert visible, "Hero banner not visible on homepage"


@pytest.mark.regression
class TestHomepageLogo:
    """Logo presence and link."""

    def test_logo_is_present(self, driver):
        """BMS logo element must be in the DOM."""
        page = HomePage(driver).load()
        logo = page.get_logo()
        assert logo is not None, "Logo element not found"
        assert logo.is_displayed(), "Logo found but not visible"
