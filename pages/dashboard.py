from .orders_history import OrdersHistoryPage

class DashboardPage:
    # constructor
    def __init__(self, page):
        self.page = page  # this will have access to this entire page

    def select_orders_navigation(self):
        self.page.get_by_role("button", name="ORDERS").click()
        return OrdersHistoryPage(self.page)
