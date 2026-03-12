# ─────────────────────────────────────────────────────────
#  Reusable helpers: retry decorator, JS utilities, waits
# ─────────────────────────────────────────────────────────

import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry(times=3, delay=1, exceptions=(Exception,)):
    """Decorator – retry a flaky action up to *times* attempts."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    logger.warning(f"[retry {attempt}/{times}] {fn.__name__} failed: {e}")
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator


def scroll_to_bottom(driver, pause: float = 0.8, max_scrolls: int = 20) -> int:
   
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0

    while scrolls < max_scrolls:
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scrolls += 1

    logger.info(f"Scrolled {scrolls} times, final height: {last_height}px")
    return last_height

def scroll_to_element(driver, element, behavior: str = "smooth"):
    driver.execute_script(
        f"arguments[0].scrollIntoView({{behavior: '{behavior}', block: 'center'}});",
        element,
    )
    time.sleep(0.4)


def get_scroll_position(driver) -> int:
    return driver.execute_script("return window.pageYOffset;")


def scroll_to_top(driver):
    driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
    time.sleep(0.5)


def wait_for_page_load(driver, timeout: int = 10):
    """Block until document.readyState === 'complete'."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        state = driver.execute_script("return document.readyState")
        if state == "complete":
            return
        time.sleep(0.3)
    raise TimeoutError("Page did not reach readyState=complete")
