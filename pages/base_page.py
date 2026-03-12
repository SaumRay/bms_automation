
import time
import logging
from pathlib import Path
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

from utils.config import EXPLICIT_WAIT
from utils.helpers import scroll_to_element

logger = logging.getLogger(__name__)

SCREENSHOTS_DIR = Path(__file__).parent.parent / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    # Navigation 
    def open(self, url: str):
        logger.info(f"Opening: {url}")
        self.driver.get(url)
        time.sleep(1)  # brief settle after navigation

    def get_title(self) -> str:
        return self.driver.title

    def get_url(self) -> str:
        return self.driver.current_url

    def go_back(self):
        self.driver.back()
        time.sleep(0.8)

    # Waits
    def wait_for_element(self, locator: tuple, timeout: int = EXPLICIT_WAIT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_visible(self, locator: tuple, timeout: int = EXPLICIT_WAIT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = EXPLICIT_WAIT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_elements(self, locator: tuple, timeout: int = EXPLICIT_WAIT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def is_element_visible(self, locator: tuple, timeout: int = 4) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # Clicks
    def click(self, locator: tuple):
        el = self.wait_for_clickable(locator)
        try:
            el.click()
        except ElementClickInterceptedException:
            # Fallback: JS click (useful when overlays block)
            logger.warning(f"Normal click intercepted on {locator}, using JS click")
            self.driver.execute_script("arguments[0].click();", el)

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    # Input
    def type_text(self, locator: tuple, text: str, clear_first: bool = True):
        el = self.wait_for_visible(locator)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.wait_for_visible(locator).text.strip()

    def get_attribute(self, locator: tuple, attr: str) -> str:
        return self.wait_for_element(locator).get_attribute(attr)

    # Hover
    def hover(self, locator: tuple):
        el = self.wait_for_visible(locator)
        ActionChains(self.driver).move_to_element(el).perform()
        time.sleep(0.3)

    # Scroll
    def scroll_to(self, locator: tuple):
        el = self.wait_for_element(locator)
        scroll_to_element(self.driver, el)
        return el

    def scroll_by_pixels(self, px: int):
        self.driver.execute_script(f"window.scrollBy(0, {px});")
        time.sleep(0.4)

    def get_scroll_y(self) -> int:
        return self.driver.execute_script("return window.pageYOffset;")

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(0.8)

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)

    # Screenshot
    def take_screenshot(self, name: str = "") -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        label = f"{name}_{ts}" if name else ts
        path = SCREENSHOTS_DIR / f"{label}.png"
        self.driver.save_screenshot(str(path))
        logger.info(f"Screenshot saved: {path}")
        return str(path)

    # JS Helpers 
    def execute_js(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    def count_elements(self, locator: tuple) -> int:
        try:
            els = self.driver.find_elements(*locator)
            return len(els)
        except NoSuchElementException:
            return 0
