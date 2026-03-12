# 🎬 BookMyShow – Selenium + Python + Pytest Automation Suite

Real-world UI automation project targeting **BookMyShow** (bookmyshow.com).

## 📁 Project Structure
```
bms_automation/
├── conftest.py              # Fixtures: browser setup/teardown, screenshots on fail
├── pytest.ini               # Pytest config, HTML report, markers
├── requirements.txt         # All dependencies
│
├── pages/                   # Page Object Model (POM)
│   ├── base_page.py         # Shared methods: scroll, wait, click, screenshot
│   ├── home_page.py         # Homepage: nav, city selector, search bar
│   ├── movies_page.py       # Movies listing: filters, cards, scroll-load
│   └── search_page.py       # Search: suggestions, keyboard nav
│
├── tests/                   # Test suites
│   ├── test_homepage.py     # Homepage load, hero banner, nav links
│   ├── test_navigation.py   # City change, menu tabs, scroll behavior
│   ├── test_search.py       # Search input, autocomplete, results
│   ├── test_movies.py       # Movies page: filters, card clicks, scroll
│   └── test_scroll.py       # Infinite scroll & lazy-load tests
│
├── utils/
│   ├── config.py            # URLs, timeouts, browser settings
│   └── helpers.py           # Retry decorator, wait helpers, JS scroll
│
├── screenshots/             # Auto-saved on test failure
└── reports/                 # HTML report output
```

## ⚙️ Setup

```bash
# 1. Clone / unzip the project
cd bms_automation

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## ▶️ Run Tests

```bash
# Run ALL tests (headless by default)
pytest

# Run with visible browser
pytest --headed

# Run a specific test file
pytest tests/test_homepage.py -v

# Run by marker (smoke / regression / scroll)
pytest -m smoke -v
pytest -m regression -v

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Run in parallel (4 workers)
pytest -n 4
```

## 🧪 What's Tested

| Test | Description |
|------|-------------|
| Homepage Load | Title, hero banner visible, page fully loaded |
| Navigation Bar | Movies / Stream / Events / Plays tabs clickable |
| City Selector | Opens city modal, selects a city, URL updates |
| Search Bar | Focus, type query, autocomplete dropdown appears |
| Search Results | Navigate to results page, result cards visible |
| Scroll Behavior | Smooth scroll to footer, back-to-top button |
| Lazy Load | Scroll down movies page → new cards load dynamically |
| Movie Card | Hover effect, click → detail page opens |
| Filter Panel | Genre / Language filters toggle correctly |
| Keyboard Navigation | Tab / Enter / Escape on search and modals |

## 📸 Screenshots
Automatically captured on every test failure and saved to `screenshots/`.
