# utils/config.py
# ─────────────────────────────────────────────────────────
#  Central config – change BASE_URL / timeouts here only
# ─────────────────────────────────────────────────────────

BASE_URL        = "https://in.bookmyshow.com"
MOVIES_URL      = f"{BASE_URL}/explore/movies-mumbai"
EVENTS_URL      = f"{BASE_URL}/explore/events-mumbai"

# Timeouts (seconds)
IMPLICIT_WAIT   = 5
EXPLICIT_WAIT   = 15
PAGE_LOAD_TIMEOUT = 60

# Browser options
HEADLESS        = False          # Set False to watch the browser
WINDOW_WIDTH    = 1440
WINDOW_HEIGHT   = 900

# Scroll
SCROLL_PAUSE    = 0.8           # seconds between scroll steps
SCROLL_STEP_PX  = 500           # pixels per scroll step
