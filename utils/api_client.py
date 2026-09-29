from playwright.sync_api import APIRequestContext, Playwright

from .config import get_base_url, get_credentials

PAYLOAD_DATA = {
    "orders": [
        {
            "country": "Albania",
            "productOrderedId": "6960eac0c941646b7a8b3e68",
        }
    ]
}


class ApiClient:
    def _request_context(self, playwright: Playwright) -> APIRequestContext:
        return playwright.request.new_context(
            base_url=get_base_url(),
            ignore_https_errors=True,
        )

    def get_token(
        self,
        playwright: Playwright,
        user_credentials: dict[str, str] | None = None,
    ) -> str:
        credentials = user_credentials or get_credentials()
        context = self._request_context(playwright)
        try:
            response = context.post(
                "/api/ecom/auth/login",
                data=credentials,
            )
            if not response.ok:
                raise RuntimeError(
                    f"Authentication failed with HTTP {response.status}: "
                    f"{response.text()}"
                )
            token = response.json().get("token")
            if not token:
                raise RuntimeError("Authentication response did not contain a token.")
            return token
        finally:
            context.dispose()

    def create_order(
        self,
        playwright: Playwright,
        user_credentials: dict[str, str] | None = None,
    ) -> str:
        token = self.get_token(playwright, user_credentials)
        context = self._request_context(playwright)
        try:
            response = context.post(
                "/api/ecom/order/create-order",
                data=PAYLOAD_DATA,
                headers={"Authorization": token},
            )
            if not response.ok:
                raise RuntimeError(
                    f"Order creation failed with HTTP {response.status}: "
                    f"{response.text()}"
                )
            order_id = response.json().get("orders", [None])[0]
            if not order_id:
                raise RuntimeError("Order response did not contain an order ID.")
            return order_id
        finally:
            context.dispose()
