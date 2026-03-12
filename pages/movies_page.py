
import time
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.config import MOVIES_URL
from utils.helpers import scroll_to_bottom

logger = logging.getLogger(__name__)

class MoviesPage(BasePage):
    # Locators 
    PAGE_HEADING     = (By.XPATH, "//h1 | //h2[contains(text(),'Movies')]")
    MOVIE_CARDS      = (By.CSS_SELECTOR,
                        "[class*='movie-card'], [class*='MovieCard'], "
                        "[class*='__card'], a[class*='card'], "
                        "div[class*='card-container'] a")
    FILTER_LANGUAGE  = (By.XPATH,
                        "//span[contains(text(),'Language')] | "
                        "//button[contains(text(),'Language')]")
    FILTER_GENRE     = (By.XPATH,
                        "//span[contains(text(),'Genre')] | "
                        "//button[contains(text(),'Genre')]")
    FILTER_FORMAT    = (By.XPATH,
                        "//span[contains(text(),'Format')] | "
                        "//button[contains(text(),'Format')]")
    FILTER_CHIPS     = (By.CSS_SELECTOR,
                        "[class*='filter'], [class*='chip'], [class*='pill']")
    SORT_BUTTON      = (By.XPATH,
                        "//span[contains(text(),'Sort')] | "
                        "//button[contains(text(),'Sort')]")
    MOVIE_TITLE      = (By.CSS_SELECTOR,
                        "[class*='title'], [class*='movie-name'], h3, h4")
    MOVIE_RATING     = (By.CSS_SELECTOR,
                        "[class*='rating'], [class*='score']")
    LOAD_MORE_BTN    = (By.XPATH,
                        "//button[contains(text(),'Load More')] | "
                        "//a[contains(text(),'Load More')]")
    BACK_TO_TOP_BTN  = (By.CSS_SELECTOR,
                        "[class*='back-to-top'], [class*='backToTop'], "
                        "button[aria-label*='top']")

    def __init__(self, driver):
        super().__init__(driver)

    # Navigation 
    def load(self):
        self.open(MOVIES_URL)
        time.sleep(2)
        return self

    def is_loaded(self) -> bool:
        return "movies" in self.get_url().lower()

    # Card interactions 
    def get_movie_cards(self):
        try:
            return self.wait_for_elements(self.MOVIE_CARDS, timeout=10)
        except TimeoutException:
            return []

    def count_movie_cards(self) -> int:
        return len(self.get_movie_cards())

    def click_first_movie(self):
        cards = self.get_movie_cards()
        if not cards:
            raise AssertionError("No movie cards found on Movies page")
        self.js_click(cards[0])
        time.sleep(2)

    def hover_over_movie(self, index: int = 0):
        cards = self.get_movie_cards()
        if index < len(cards):
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(self.driver).move_to_element(cards[index]).perform()
            time.sleep(0.5)

    # Filters 
    def click_language_filter(self) -> bool:
        try:
            self.click(self.FILTER_LANGUAGE)
            time.sleep(0.8)
            return True
        except Exception:
            return False

    def click_genre_filter(self) -> bool:
        try:
            self.click(self.FILTER_GENRE)
            time.sleep(0.8)
            return True
        except Exception:
            return False

    def get_active_filters(self) -> list:
        chips = self.driver.find_elements(*self.FILTER_CHIPS)
        return [c.text for c in chips if c.text.strip()]

    # Scroll / Lazy load
    def scroll_and_count_cards(self, scroll_steps: int = 5) -> dict:
        """
        Scroll down in increments, record card count at each step.
        Returns dict: {step: card_count}
        """
        results = {}
        cards_before = self.count_movie_cards()
        results[0] = cards_before
        logger.info(f"Cards before scroll: {cards_before}")

        for step in range(1, scroll_steps + 1):
            self.scroll_by_pixels(700)
            time.sleep(1.2)
            count = self.count_movie_cards()
            results[step] = count
            logger.info(f"Step {step}: {count} cards visible")

        return results

    def scroll_to_page_bottom_and_count(self) -> tuple:
        """Scroll to bottom, return (cards_before, cards_after)."""
        before = self.count_movie_cards()
        scroll_to_bottom(self.driver, pause=1.2)
        time.sleep(1.5)
        after = self.count_movie_cards()
        logger.info(f"Cards before: {before}, after scroll: {after}")
        return before, after

    def is_back_to_top_visible(self) -> bool:
        return self.is_element_visible(self.BACK_TO_TOP_BTN, timeout=4)

    def click_back_to_top(self):
        if self.is_back_to_top_visible():
            self.click(self.BACK_TO_TOP_BTN)
            time.sleep(1)
            return True
        return False

    def load_more_if_available(self) -> bool:
        try:
            self.click(self.LOAD_MORE_BTN)
            time.sleep(2)
            return True
        except Exception:
            return False
