import os


DEFAULT_BASE_URL = "https://rahulshettyacademy.com"
DEFAULT_CLIENT_PATH = "/client/"


def get_base_url() -> str:
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def get_client_url() -> str:
    return f"{get_base_url()}{DEFAULT_CLIENT_PATH}"


def get_app_url(path: str) -> str:
    return f"{get_base_url()}/{path.lstrip('/')}"


def get_credentials() -> dict[str, str]:
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    if not email or not password:
        raise RuntimeError(
            "Set TEST_USER_EMAIL and TEST_USER_PASSWORD before running "
            "tests that require an authenticated account."
        )
    return {"userEmail": email, "userPassword": password}


def get_practice_credentials() -> dict[str, str]:
    username = os.getenv("PRACTICE_USERNAME")
    password = os.getenv("PRACTICE_PASSWORD")
    if not username or not password:
        raise RuntimeError(
            "Set PRACTICE_USERNAME and PRACTICE_PASSWORD before running "
            "practice login tests."
        )
    return {"username": username, "password": password}
