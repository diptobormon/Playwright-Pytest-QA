#testing edge cases
#network interception - intercepting responses, intercepting requests
from playwright.sync_api import Page, expect
from utils.config import get_app_url, get_base_url

fakePayloadOrderResponse = {"data":[],"message":"No Orders"}

def intercept_response(route):
    route.fulfill(
        json= fakePayloadOrderResponse)

def test_network_response_interception(page: Page, authenticated_credentials):
    credentials = authenticated_credentials
    page.goto(get_app_url("/client/"))
    page.route(
        f"{get_base_url()}/api/ecom/order/get-orders-for-customer/*",
        intercept_response,
    )
    page.get_by_placeholder("email@example.com").fill(credentials["userEmail"])
    page.get_by_placeholder("enter your passsword").fill(credentials["userPassword"])
    page.get_by_role("button", name="Login").click()

    page.get_by_role("button", name="ORDERS").click()  #line 14 is provoked here
    expect(page.locator(".mt-4")).to_contain_text("No Orders")
    #event handler - route() #no orders made
