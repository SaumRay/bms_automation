# ─────────────────────────────────────────────────────────
#  Pytest fixtures: browser setup, teardown, auto-screenshot
#  - Uses undetected-chromedriver to bypass bot detection
#  - Auto-detects CI environment and forces headless
#  - Saves screenshot on every test failure
# ─────────────────────────────────────────────────────────

import sys
import os
import pytest
import logging
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

import undetected_chromedriver as uc
from utils.config import HEADLESS, WINDOW_WIDTH, WINDOW_HEIGHT, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT

logger = logging.getLogger(__name__)

SCREENSHOTS_DIR = Path("screenshots")
SCREENSHOTS_DIR.mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

# Auto-detect GitHub Actions / any CI environment
IS_CI = os.getenv("CI", "false").lower() == "true"

# Browser fixture
@pytest.fixture(scope="function")
def driver(request):

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.page_load_strategy = 'eager'

    # Always headless on CI, respect config locally
    if HEADLESS or IS_CI:
        chrome_options.add_argument("--headless=new")

    # Required for Linux / GitHub Actions
    if IS_CI:
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")

    driver = uc.Chrome(options=chrome_options, version_main=145)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    logger.info(f"Browser started ✔  [CI={IS_CI}, headless={HEADLESS or IS_CI}]")
    yield driver

    # Teardown: screenshot on failure 
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = request.node.name.replace(" ", "_")
        path = SCREENSHOTS_DIR / f"FAIL_{name}_{ts}.png"
        try:
            driver.save_screenshot(str(path))
            logger.info(f"Failure screenshot saved: {path}")
        except Exception as e:
            logger.warning(f"Could not save screenshot: {e}")

    try:
        driver.quit()
    except Exception:
        pass
    logger.info("Browser closed ✔")


# Hook: capture pass/fail status for screenshot logic
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)