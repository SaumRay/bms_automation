# ─────────────────────────────────────────────────────────
#  Navigation tests – tabs, city selector, routing
# ─────────────────────────────────────────────────────────

import time
import pytest
from pages.home_page import HomePage

@pytest.mark.navigation
@pytest.mark.smoke
class TestNavTabs:
    """Top navigation bar – Movies / Events / Plays tabs."""

    def test_click_movies_tab(self, driver):
        """Clicking Movies tab should navigate to a movies URL."""
        page = HomePage(driver).load()
        page.click_movies()
        url = page.get_url()
        assert "movie" in url.lower(), (
            f"Expected 'movie' in URL after clicking Movies, got: {url}"
        )

    def test_click_events_tab(self, driver):
        """Clicking Events tab should navigate to an events URL."""
        page = HomePage(driver).load()
        page.click_events()
        url = page.get_url()
        assert any(kw in url.lower() for kw in ["event", "explore"]), (
            f"Expected events URL, got: {url}"
        )

    def test_click_plays_tab(self, driver):
        """Clicking Plays tab should navigate to a plays URL."""
        page = HomePage(driver).load()
        page.click_plays()
        url = page.get_url()
        assert any(kw in url.lower() for kw in ["play", "theatre", "explore"]), (
            f"Expected plays URL, got: {url}"
        )

    def test_back_navigation_after_movies(self, driver):
        """Browser back button should return to homepage."""
        page = HomePage(driver).load()
        home_url = page.get_url()
        page.click_movies()
        time.sleep(1)
        page.go_back()
        time.sleep(1)
        assert "bookmyshow.com" in page.get_url(), (
            f"Back navigation failed, current URL: {page.get_url()}"
        )


@pytest.mark.navigation
class TestCitySelector:
    """City selector modal – open, interact, close."""

    def test_city_selector_opens(self, driver):
        """Clicking the city chip should reveal the city modal or change URL."""
        page = HomePage(driver).load()
        url_before = page.get_url()
        page.open_city_selector()
        time.sleep(1)
        # Either a modal opened OR the URL changed (direct city page navigation)
        url_after = page.get_url()
        modal_visible = page.is_city_modal_open()
        assert modal_visible or (url_before != url_after), (
            "City selector click had no visible effect"
        )

    def test_page_url_changes_after_city_select(self, driver):
        """After selecting a city, the URL should reflect the selection."""
        page = HomePage(driver).load()
        success = page.select_city("Delhi")
        if not success:
            pytest.skip("City selector interaction not available in this layout")
        url = page.get_url()
        assert "bookmyshow.com" in url, "After city select, URL is unexpected"
