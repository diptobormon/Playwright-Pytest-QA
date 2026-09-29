# 🎭 Playwright Pytest Automation Suite

> A personal end-to-end test automation project built with **Python**, **Pytest**, and **Playwright**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.58.0-2EAD33?style=flat&logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-9.0.2-0A9EDC?style=flat&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

---

## 📌 Overview

This portfolio project demonstrates practical UI, API, Page Object Model, and network-interception testing against the Rahul Shetty Academy demo applications. It is designed for repeatable local execution and GitHub Actions. It is not a production-system certification suite; production release decisions require a controlled staging environment and application-specific test data.

**Key highlights:**
- Clean separation of concerns via Page Object Model
- Parallel test execution with `pytest-xdist`
- HTML reporting with `pytest-html` and metadata support
- Configurable base URL for multi-environment testing
- Headless and headed browser support through `pytest-playwright`
- Reusable utility functions and shared fixtures via `conftest.py`
- Credentials loaded from environment variables instead of source code

---

## 🛠 Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core language |
| Playwright | 1.58.0 | Browser automation |
| Pytest | 9.0.2 | Test runner & framework |
| pytest-playwright | 0.7.2 | Playwright–Pytest integration |
| pytest-xdist | 3.8.0 | Parallel test execution |
| pytest-html | 4.2.0 | HTML test reporting |
| pytest-base-url | 2.1.0 | Configurable base URL |
| pytest-metadata | 3.1.1 | Report metadata enrichment |

---

## 📁 Project Structure

```
playwright-pytest-automation/
│
├── pages/              # Page Object Models (one class per page)
├── tests/              # Test files (organized by feature/module)
├── utils/              # Reusable helper functions and constants
├── assets/             # Static test assets (images, files, etc.)
│
├── conftest.py         # Shared fixtures and Playwright setup
├── pytest.ini          # Pytest configuration (markers, base URL, options)
├── requirements.txt    # Pinned Python dependencies
├── .env.example        # Safe configuration template (no secrets)
└── README.md
```

**Design pattern:** Each page of the application under test has a corresponding class in `pages/` that encapsulates its locators and actions. Tests in `tests/` interact only with page objects — keeping tests clean and maintainable.

---

## ⚙️ Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
# 1. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install
```

### Test account configuration

Authenticated API/UI tests require a dedicated non-production test account. Never commit a
real password, token, or `.env` file.

```bash
# Export these values in your shell or configure them in your CI secret store.
TEST_USER_EMAIL=your-test-account@example.com
TEST_USER_PASSWORD=replace-with-a-test-password
PRACTICE_USERNAME=your-practice-username
PRACTICE_PASSWORD=replace-with-a-practice-password
BASE_URL=https://rahulshettyacademy.com
```

The project reads the credential variables and `BASE_URL` from the environment.
`.env.example` is a template only; the project does not load `.env` files automatically.
Tests that require credentials are skipped with a clear message when the corresponding
environment variables are not configured. The default GitHub Actions workflow currently
runs without credentials and therefore validates only unauthenticated coverage.

Use dedicated, isolated test accounts for `TEST_USER_*` and `PRACTICE_*`. The API tests
create orders in the target environment and do not delete them because the demo API does
not expose a supported cleanup endpoint. Do not point these tests at a production account.
When authenticated coverage is needed later, add the four variables as GitHub Actions
repository secrets and pass them into the workflow environment.

---

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_ui_validations.py

# Run with browser visible (headed mode)
pytest --headed

# Run tests in parallel (4 workers)
pytest -n 4

# Run on a specific browser
pytest --browser firefox
pytest --browser webkit

# Generate an HTML report
pytest --html=reports/report.html --self-contained-html

# Run against a different environment
pytest --base-url https://staging.example.com

# Combine options
pytest --headed --browser chromium -n 2 --html=reports/report.html
```

The custom `browser_instance` fixture uses the standard `pytest-playwright` browser and
`pytest-base-url` configuration, so `--browser`, `--headed`, and `--base-url` apply consistently.

---

## 📊 Test Reports

After running tests with the `--html` flag, open the generated report in your browser:

```bash
# Example
pytest --html=reports/report.html --self-contained-html
open reports/report.html        # macOS
start reports/report.html       # Windows
```

Reports include test status, duration, traces retained on failure, and environment metadata.
The CI workflow uploads both the HTML report and the `test-results/` Playwright artifacts.

---

## 🧩 Key Concepts

### Page Object Model
Each page is represented as a Python class with locators and action methods:

```python
# pages/login_page.py (example)
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

### Fixtures (`conftest.py`)
Shared setup and teardown logic (browser launch, page creation, test data) is centralised in `conftest.py` and injected into tests via Pytest fixtures.

---

## 🚀 CI/CD Integration

This framework is CI/CD ready. Example GitHub Actions workflow:

```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps
      - name: Run tests
        env:
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
          PRACTICE_USERNAME: ${{ secrets.PRACTICE_USERNAME }}
          PRACTICE_PASSWORD: ${{ secrets.PRACTICE_PASSWORD }}
        run: pytest --tracing=retain-on-failure --html=report.html --self-contained-html
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: test-report
          path: report.html
      - name: Upload Playwright artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-test-results
          path: test-results/
          if-no-files-found: ignore
```

---

## 📂 Writing a New Test

1. Create a page object in `pages/` if the page isn't already covered.
2. Add your test file in `tests/` following the naming convention `test_<feature>.py`.
3. Use fixtures from `conftest.py` for browser and page setup.
4. Run and verify locally before pushing.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 👤 Author

**Dipto Bormon**

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
