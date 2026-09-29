#API testing e2e  - e-commerce website
#API and UI testing - login and create an order
#use selectorshub plugin in browser tools
from playwright.sync_api import Playwright, expect
from utils.api_client import ApiClient
from utils.config import get_client_url

def test_end_to_end_web_api(playwright: Playwright, page, authenticated_credentials):
    user_credentials = authenticated_credentials
    api_client = ApiClient()
    order_id = api_client.create_order(playwright, user_credentials)
    page.goto(get_client_url())
    page.get_by_placeholder("email@example.com").fill(user_credentials["userEmail"])
    page.get_by_placeholder("enter your passsword").fill(user_credentials["userPassword"])
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="ORDERS").click()
    row = page.locator("tr").filter(has_text=order_id)
    row.get_by_role("button", name="View").click()
    expect(page.locator(".tagline")).to_contain_text("Thank you for Shopping With Us")