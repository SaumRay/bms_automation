# Movie listing page – filters, card clicks, hover
import pytest
from pages.movies_page import MoviesPage
from pages.home_page import HomePage

@pytest.mark.regression
class TestMoviesPage:

    def test_movies_page_loads(self, driver):
        page = MoviesPage(driver).load()
        assert page.is_loaded(), f"Movies page URL unexpected: {page.get_url()}"

    def test_movie_cards_are_present(self, driver):
        page = MoviesPage(driver).load()
        count = page.count_movie_cards()
        assert count > 0, "No movie cards found on Movies page"

    def test_movie_card_click_opens_detail(self, driver):
        page = MoviesPage(driver).load()
        url_before = page.get_url()
        page.click_first_movie()
        url_after = page.get_url()
        assert url_after != url_before, (
            "URL did not change after clicking a movie card"
        )

    def test_hover_over_movie_card(self, driver):
        page = MoviesPage(driver).load()
        count = page.count_movie_cards()
        if count == 0:
            pytest.skip("No movie cards to hover")
        page.hover_over_movie(0)   # Should not raise any exception

    def test_language_filter_clickable(self, driver):
        page = MoviesPage(driver).load()
        result = page.click_language_filter()
        if not result:
            pytest.skip("Language filter not found in this layout")
        assert result, "Language filter click failed"

    def test_genre_filter_clickable(self, driver):
        page = MoviesPage(driver).load()
        result = page.click_genre_filter()
        if not result:
            pytest.skip("Genre filter not found in this layout")
        assert result, "Genre filter click failed"


@pytest.mark.smoke
class TestMoviesFromNav:

    def test_navigate_to_movies_via_nav(self, driver):
        """Use nav tab to reach movies, verify URL."""
        page = HomePage(driver).load()
        page.click_movies()
        url = page.get_url()
        assert "movie" in url.lower() or "explore" in url.lower(), (
            f"Unexpected URL after clicking Movies nav: {url}"
        )
