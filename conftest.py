import os

import pytest

from utils.config import get_credentials, get_practice_credentials


@pytest.fixture(scope="session")
def authenticated_credentials():
    try:
        return get_credentials()
    except RuntimeError as error:
        if os.getenv("CI") == "true":
            raise
        pytest.skip(str(error))


@pytest.fixture(scope="session")
def practice_credentials():
    try:
        return get_practice_credentials()
    except RuntimeError as error:
        if os.getenv("CI") == "true":
            raise
        pytest.skip(str(error))


@pytest.fixture(scope='function')
def browser_instance(browser, base_url):
    """Provide an isolated page while reusing pytest-playwright's browser setup."""
    context = browser.new_context(ignore_https_errors=True, base_url=base_url)
    page = context.new_page()
    yield page
    context.close()
