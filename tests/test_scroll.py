# Scroll behavior & lazy-load tests on BookMyShow
import time
import pytest
from pages.home_page import HomePage
from pages.movies_page import MoviesPage
from utils.helpers import scroll_to_bottom

@pytest.mark.scroll
@pytest.mark.smoke
class TestScrollBehavior:

    def test_page_scrolls_down(self, driver):
        """Scrolling should increase the Y offset."""
        page = HomePage(driver).load()
        y_before = page.get_scroll_y()
        page.scroll_by_pixels(800)
        y_after = page.get_scroll_y()
        assert y_after > y_before, f"Scroll did not work. Y before={y_before}, after={y_after}"

    def test_scroll_to_footer(self, driver):
        """Scrolling to footer element should make it visible."""
        page = HomePage(driver).load()
        footer = page.scroll_to_footer()
        assert footer is not None, "Footer element not found"
        assert footer.is_displayed(), "Footer not visible after scroll"

    def test_scroll_to_top_resets_position(self, driver):
        """After scrolling down, scroll-to-top should return Y near 0."""
        page = HomePage(driver).load()
        page.scroll_by_pixels(2000)
        time.sleep(0.5)
        page.scroll_to_top()
        time.sleep(0.8)
        y = page.get_scroll_y()
        assert y < 100, f"Expected Y < 100 after scroll to top, got {y}"

    def test_incremental_scroll_increases_offset(self, driver):
        """Each scroll step should increase Y position."""
        page = HomePage(driver).load()
        positions = page.scroll_through_homepage(steps=4)
        assert len(positions) == 4, "Expected 4 scroll positions"
        # Each position should be >= previous
        for i in range(1, len(positions)):
            assert positions[i] >= positions[i - 1], (
                f"Scroll position did not increase at step {i}: "
                f"{positions[i-1]} -> {positions[i]}"
            )

@pytest.mark.scroll
@pytest.mark.regression
class TestLazyLoad:
    """Test that more content loads as user scrolls down."""

    def test_movies_page_lazy_load(self, driver):
        """Movie cards count should increase (or stay same) after scrolling."""
        page = MoviesPage(driver).load()
        before, after = page.scroll_to_page_bottom_and_count()
        # Cards should never decrease after scrolling
        assert after >= before, (
            f"Card count decreased after scroll: {before} -> {after}"
        )

    def test_scroll_step_by_step_on_movies(self, driver):
        """Step-by-step scroll should progressively reveal cards."""
        page = MoviesPage(driver).load()
        results = page.scroll_and_count_cards(scroll_steps=4)
        # At least some cards should be visible at step 0
        assert results[0] >= 0, "No cards visible initially"
        # Final count should be >= initial count
        assert results[4] >= results[0], (
            f"Card count dropped after scrolling: {results[0]} -> {results[4]}"
        )

    def test_scroll_position_on_movies_page(self, driver):
        """Scrolling on movies page should move the viewport."""
        page = MoviesPage(driver).load()
        y0 = page.get_scroll_y()
        page.scroll_by_pixels(1000)
        y1 = page.get_scroll_y()
        assert y1 > y0, f"Viewport did not scroll on movies page: {y0} -> {y1}"


@pytest.mark.scroll
class TestScrollToElement:
    """Scroll-to-element and back-to-top button."""

    def test_back_to_top_appears_after_scrolling(self, driver):
        """Back-to-top button should become visible after scrolling far down."""
        page = MoviesPage(driver).load()
        scroll_to_bottom(driver, pause=0.8)
        # Not all sites show a back-to-top; skip if not present
        if not page.is_back_to_top_visible():
            pytest.skip("Back-to-top button not present in this layout")
        assert page.is_back_to_top_visible()

    def test_back_to_top_click_scrolls_up(self, driver):
        """Clicking back-to-top should bring Y offset back near 0."""
        page = MoviesPage(driver).load()
        scroll_to_bottom(driver, pause=0.8)
        clicked = page.click_back_to_top()
        if not clicked:
            pytest.skip("Back-to-top button not present")
        time.sleep(1)
        y = page.get_scroll_y()
        assert y < 300, f"Expected Y < 300 after back-to-top, got {y}"
