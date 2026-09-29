#testing edge cases
#network interception - intercepting responses, intercepting requests
from playwright.sync_api import Page, expect, Playwright
from utils.api_client import ApiClient
from utils.config import get_app_url, get_base_url

def intercept_request(route):
    route.continue_(
        url=(
            f"{get_base_url()}/api/ecom/order/"
            "get-orders-details?id=69e62b74f86ba51a6576422c"
        )
    )
    # Use a different order ID to exercise the authorization error path.


def test_network_request_interception(page: Page, authenticated_credentials):
    credentials = authenticated_credentials
    page.goto(get_app_url("/client/"))
    page.route(
        f"{get_base_url()}/api/ecom/order/get-orders-details?id=*",
        intercept_request,
    )
    page.get_by_placeholder("email@example.com").fill(credentials["userEmail"])
    page.get_by_placeholder("enter your passsword").fill(credentials["userPassword"])
    page.get_by_role("button", name="Login").click()

    page.get_by_role("button", name="ORDERS").click()
    page.get_by_role("button", name="View").first.click()   #line 14 is provoked here
    expect(page.locator(".blink_me")).to_contain_text(
        "not authorize to view this order"
    )

def test_session_storage_authentication(playwright: Playwright, authenticated_credentials):
    api_client = ApiClient()
    token = api_client.get_token(playwright, authenticated_credentials)
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.add_init_script(f"""localStorage.setItem("token", "{token}")""")
    page.goto(get_app_url("/client"))
    page.get_by_role("button", name="ORDERS").click()
    expect(page.get_by_text('Your Orders')).to_be_visible()
    context.close()
    browser.close()
