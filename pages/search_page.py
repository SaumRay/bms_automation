
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class SearchPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR,
                    "input[placeholder*='Search for Movies'],"
                    "input[placeholder*='Search'],"
                    "input[class*='sc-'][type='text'],"
                    "input[type='search']")

    SEARCH_WRAPPER = (By.CSS_SELECTOR,
                      "[class*='search__InputWrapper'],"
                      "[class*='SearchBar'],"
                      "[class*='searchBar'],"
                      "div[class*='search']")

    AUTOCOMPLETE_DROPDOWN = (By.CSS_SELECTOR,
                              "[class*='suggestion'],"
                              "[class*='Suggestion'],"
                              "[class*='autocomplete'],"
                              "[class*='SearchSuggestion'],"
                              "ul[class*='search']")

    AUTOCOMPLETE_ITEMS = (By.CSS_SELECTOR,
                          "[class*='suggestion'] li,"
                          "[class*='Suggestion'] li,"
                          "[class*='suggestion-item'],"
                          "[class*='SuggestionItem'],"
                          "li[class*='search']")

    RESULT_CARDS = (By.CSS_SELECTOR,
                    "[class*='result-card'],"
                    "[class*='ResultCard'],"
                    "[class*='search-card']")

    NO_RESULTS_MSG = (By.XPATH,
                      "//*[contains(text(),'No results')]|"
                      "//*[contains(text(),'no results')]|"
                      "//*[contains(text(),'Nothing found')]")

    def __init__(self, driver):
        super().__init__(driver)

    # Find search input robustly
    def _find_search_input(self):
        """Trying multiple strategies to locate the search input."""
        # Strategy 1: direct CSS
        try:
            el = self.wait_for_visible(self.SEARCH_INPUT, timeout=5)
            if el and el.is_displayed():
                return el
        except TimeoutException:
            pass

        # Strategy 2: click the search icon first, then find input
        try:
            icons = self.driver.find_elements(
                By.CSS_SELECTOR,
                "button[class*='search'], span[class*='search'], "
                "div[class*='search__Icon'], svg[class*='search']"
            )
            for icon in icons:
                try:
                    icon.click()
                    time.sleep(0.8)
                    break
                except Exception:
                    continue
            el = self.wait_for_visible(self.SEARCH_INPUT, timeout=5)
            if el:
                return el
        except TimeoutException:
            pass

        # Strategy 3: find ANY visible text input
        try:
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input:not([type])")
            for inp in inputs:
                if inp.is_displayed():
                    logger.info(f"Found input via fallback: placeholder='{inp.get_attribute('placeholder')}'")
                    return inp
        except Exception:
            pass

        raise TimeoutException("Could not find search input on BMS page")

    def focus_search_input(self):
        return self._find_search_input()

    # Core actions 
    def search_for(self, query: str, press_enter: bool = True):
        inp = self._find_search_input()
        inp.clear()
        inp.send_keys(query)
        time.sleep(2)
        if press_enter:
            inp.send_keys(Keys.RETURN)
            time.sleep(2.5)
        return self

    def get_autocomplete_suggestions(self) -> list:
        try:
            items = self.wait_for_elements(self.AUTOCOMPLETE_ITEMS, timeout=5)
            texts = [i.text.strip() for i in items if i.text.strip()]
            logger.info(f"Suggestions: {texts}")
            return texts
        except TimeoutException:
            logger.warning("No autocomplete items found")
            return []

    def click_first_suggestion(self) -> bool:
        suggestions = self.get_autocomplete_suggestions()
        if not suggestions:
            return False
        items = self.driver.find_elements(*self.AUTOCOMPLETE_ITEMS)
        if items:
            self.js_click(items[0])
            time.sleep(2)
            return True
        return False

    def press_escape_to_close(self):
        try:
            inp = self._find_search_input()
            inp.send_keys(Keys.ESCAPE)
            time.sleep(0.5)
        except Exception:
            pass

    def clear_search_input(self):
        try:
            inp = self._find_search_input()
            inp.clear()
            time.sleep(0.3)
        except Exception:
            pass

    # Assertions 
    def is_autocomplete_visible(self) -> bool:
        return self.is_element_visible(self.AUTOCOMPLETE_DROPDOWN, timeout=5)

    def count_result_cards(self) -> int:
        return self.count_elements(self.RESULT_CARDS)

    def is_on_search_results_page(self) -> bool:
        return "search" in self.get_url().lower()

    def has_no_results_message(self) -> bool:
        return self.is_element_visible(self.NO_RESULTS_MSG, timeout=4)

    def navigate_suggestions_with_keyboard(self, steps: int = 2):
        inp = self._find_search_input()
        focused_texts = []
        for _ in range(steps):
            inp.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            try:
                active = self.driver.execute_script("return document.activeElement.innerText;")
                focused_texts.append(active)
            except Exception:
                pass
        return focused_texts