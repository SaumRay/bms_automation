
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.config import BASE_URL

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    # Locators
    LOGO              = (By.CSS_SELECTOR, "a.__logo, img[alt*='BookMyShow'], a[href='/']")
    SEARCH_ICON       = (By.CSS_SELECTOR, "[class*='search'], [data-testid='search-icon']")
    SEARCH_INPUT      = (By.CSS_SELECTOR, "input[placeholder*='Search'], input[type='search'], input[class*='search']")
    NAV_MOVIES        = (By.XPATH, "//a[normalize-space()='Movies'] | //span[normalize-space()='Movies']")
    NAV_STREAM        = (By.XPATH, "//a[normalize-space()='Stream'] | //span[normalize-space()='Stream']")
    NAV_EVENTS        = (By.XPATH, "//a[normalize-space()='Events'] | //span[normalize-space()='Events']")
    NAV_PLAYS         = (By.XPATH, "//a[normalize-space()='Plays'] | //span[normalize-space()='Plays']")
    NAV_SPORTS        = (By.XPATH, "//a[normalize-space()='Sports'] | //span[normalize-space()='Sports']")
    CITY_SELECTOR     = (By.CSS_SELECTOR, "[class*='cityName'], [data-testid*='city'], button[class*='city']")
    CITY_MODAL        = (By.CSS_SELECTOR, "[class*='modal'], [class*='popup'], [role='dialog']")
    CITY_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='city' i], input[placeholder*='location' i]")
    BANNER_SECTION    = (By.CSS_SELECTOR, "[class*='banner'], [class*='hero'], [class*='slider']")
    MOVIE_CARDS       = (By.CSS_SELECTOR, "[class*='movie-card'], [class*='MovieCard'], a[class*='card']")
    FOOTER            = (By.CSS_SELECTOR, "footer, [class*='footer']")
    COOKIE_CLOSE      = (By.CSS_SELECTOR, "[class*='cookie'] button, #onetrust-accept-btn-handler")

    def __init__(self, driver):
        super().__init__(driver)

    # Actions
    def load(self):
        self.open(BASE_URL)
        self._dismiss_overlays()
        return self

    def _dismiss_overlays(self):
        time.sleep(1.5)
        try:
            btn = self.driver.find_elements(*self.COOKIE_CLOSE)
            if btn:
                btn[0].click()
                logger.info("Dismissed cookie banner")
        except Exception:
            pass

    def is_loaded(self) -> bool:
        title = self.get_title().lower()
        return "bookmyshow" in title

    def get_page_title(self) -> str:
        return self.get_title()

    def get_logo(self):
        return self.wait_for_visible(self.LOGO)

    # Navigation clicks
    def click_movies(self):
        self.click(self.NAV_MOVIES)
        time.sleep(1.5)

    def click_events(self):
        self.click(self.NAV_EVENTS)
        time.sleep(1.5)

    def click_plays(self):
        self.click(self.NAV_PLAYS)
        time.sleep(1.5)

    def click_sports(self):
        try:
            self.click(self.NAV_SPORTS)
            time.sleep(1.5)
            return True
        except Exception:
            return False

    # City selector 
    def open_city_selector(self):
        self.click(self.CITY_SELECTOR)
        time.sleep(1)

    def is_city_modal_open(self) -> bool:
        return self.is_element_visible(self.CITY_MODAL, timeout=5)

    def select_city(self, city_name: str):
        self.open_city_selector()
        time.sleep(0.8)
        try:
            inp = self.wait_for_visible(self.CITY_SEARCH_INPUT, timeout=5)
            inp.clear()
            inp.send_keys(city_name)
            time.sleep(1)
            # Clicking the first suggestion that matches
            suggestion_xpath = f"//li[contains(., '{city_name}')] | //div[contains(@class,'city')][contains(., '{city_name}')]"
            suggestions = self.driver.find_elements(By.XPATH, suggestion_xpath)
            if suggestions:
                suggestions[0].click()
                time.sleep(1.5)
                logger.info(f"Selected city: {city_name}")
                return True
        except TimeoutException:
            logger.warning("City search input not found")
        return False

    # Search 
    def open_search(self):
        """Click the search icon to reveal the input."""
        try:
            self.click(self.SEARCH_ICON)
            time.sleep(0.5)
        except Exception:
            pass  # search bar may already be visible

    def type_in_search(self, query: str):
        self.open_search()
        inp = self.wait_for_visible(self.SEARCH_INPUT, timeout=8)
        inp.clear()
        inp.send_keys(query)
        time.sleep(4)

    def press_enter_on_search(self):
        inp = self.wait_for_visible(self.SEARCH_INPUT)
        inp.send_keys(Keys.RETURN)
        time.sleep(2)

    def clear_search(self):
        inp = self.wait_for_visible(self.SEARCH_INPUT)
        inp.send_keys(Keys.ESCAPE)

    # Scroll helpers
    def scroll_to_footer(self):
        footer = self.scroll_to(self.FOOTER)
        return footer

    def scroll_through_homepage(self, steps: int = 5):
        """Scroll down in increments and return list of Y positions."""
        positions = []
        for _ in range(steps):
            self.scroll_by_pixels(600)
            positions.append(self.get_scroll_y())
        return positions

    # Counts
    def count_movie_cards(self) -> int:
        return self.count_elements(self.MOVIE_CARDS)

    def is_banner_visible(self) -> bool:
        return self.is_element_visible(self.BANNER_SECTION)
