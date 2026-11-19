import uuid

from base_request import BASE_URL_PETSTORE
from user_requests import UserRequests
from store_requests import StoreRequests


def test_user_crud():
    """Проверка создания, получения, обновления и удаления пользователя."""

    api = UserRequests(BASE_URL_PETSTORE)

    username = f"student_{uuid.uuid4().hex[:10]}"

    user_data = {
        "id": 10001,
        "username": username,
        "firstName": "Ivan",
        "lastName": "Petrov",
        "email": "ivan.petrov@example.com",
        "password": "test_password_123",
        "phone": "79990000000",
        "userStatus": 1
    }

    created = False

    try:
        # POST: создание пользователя
        create_result = api.create_user(user_data)
        assert create_result["code"] == 200
        created = True

        # GET: получение пользователя
        user = api.get_user(username)
        assert user["username"] == username
        assert user["firstName"] == "Ivan"

        # PUT: обновление пользователя
        updated_data = {
            **user_data,
            "firstName": "Petr",
            "email": "petr.petrov@example.com"
        }

        api.update_user(username, updated_data)

        updated_user = api.get_user(username)
        assert updated_user["firstName"] == "Petr"
        assert updated_user["email"] == "petr.petrov@example.com"

        # DELETE: удаление пользователя
        delete_result = api.delete_user(username)
        assert delete_result["code"] == 200
        created = False

    finally:
        if created:
            api.delete_user(username)
        api.close()


def test_store_crud():
    """Проверка получения остатков и работы с заказом."""

    api = StoreRequests(BASE_URL_PETSTORE)

    order_id = uuid.uuid4().int % 1000000
    created = False

    order_data = {
        "id": order_id,
        "petId": 1,
        "quantity": 2,
        "shipDate": "2026-11-19T12:00:00.000Z",
        "status": "placed",
        "complete": True
    }

    try:
        # GET: получение остатков товаров
        inventory = api.get_inventory()
        assert isinstance(inventory, dict)
        assert len(inventory) > 0

        # POST: создание заказа
        created_order = api.create_order(order_data)
        assert created_order["id"] == order_id
        created = True

        # GET: получение заказа
        order = api.get_order(order_id)
        assert order["id"] == order_id
        assert order["quantity"] == 2
        assert order["status"] == "placed"

        # DELETE: удаление заказа
        delete_result = api.delete_order(order_id)
        assert delete_result["code"] == 200
        created = False

    finally:
        if created:
            api.delete_order(order_id)
        api.close()
