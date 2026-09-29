from .order_details import OrderDetails

class OrdersHistoryPage:

    def __init__(self, page):
        self.page = page

    def select_order(self, order_id):
        row = self.page.locator("tr").filter(has_text=order_id)
        row.get_by_role("button", name="View").click()
        return OrderDetails(self.page)