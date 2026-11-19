from base_request import BaseRequest, BASE_URL_PETSTORE


class StoreRequests(BaseRequest):
    """Запросы для работы с заказами и остатками товаров."""

    def get_inventory(self):
        """GET /store/inventory — получение остатков товаров."""
        response = self.get(
            "store/inventory",
            expected_status=200
        )
        return self.get_json(response)

    def create_order(self, order_data):
        """POST /store/order — создание заказа."""
        response = self.post(
            "store/order",
            data=order_data,
            expected_status=200
        )
        return self.get_json(response)

    def get_order(self, order_id):
        """GET /store/order/{orderId} — получение заказа."""
        response = self.get(
            f"store/order/{order_id}",
            expected_status=200
        )
        return self.get_json(response)

    def delete_order(self, order_id):
        """DELETE /store/order/{orderId} — удаление заказа."""
        response = self.delete(
            f"store/order/{order_id}",
            expected_status=200
        )
        return self.get_json(response)


if __name__ == "__main__":
    api = StoreRequests(BASE_URL_PETSTORE)

    order_id = 10002

    order_data = {
        "id": order_id,
        "petId": 1,
        "quantity": 2,
        "shipDate": "2026-11-19T12:00:00.000Z",
        "status": "placed",
        "complete": True
    }

    try:
        print("1. GET INVENTORY")
        inventory = api.get_inventory()
        print(inventory)

        print("\n2. CREATE ORDER")
        print(api.create_order(order_data))

        print("\n3. GET ORDER")
        order = api.get_order(order_id)
        print(order)

        print("\n4. DELETE ORDER")
        print(api.delete_order(order_id))

    finally:
        api.close()
