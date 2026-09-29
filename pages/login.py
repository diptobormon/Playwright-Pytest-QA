from .dashboard import DashboardPage
from utils.config import get_client_url

class LoginPage:
    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto(get_client_url(), wait_until="domcontentloaded")

    def login(self, user_email, user_password):
        self.page.get_by_placeholder("email@example.com").fill(user_email)
        self.page.get_by_placeholder("enter your passsword").fill(user_password)
        self.page.get_by_role("button", name="Login").click()
        self.page.get_by_role("button", name="ORDERS").wait_for()
        return DashboardPage(self.page)
