import uuid

import allure
import pytest
from pydantic import ValidationError

from base_request import BASE_URL_PETSTORE
from user_requests import UserRequests
from store_requests import StoreRequests
from models import User, Order


@allure.epic("Petstore API")
@allure.feature("User")
@allure.story("CRUD пользователя")
@allure.title("Создание, получение, обновление и удаление пользователя")
@allure.description(
    "Проверка полного CRUD-сценария пользователя с валидацией "
    "входных и выходных данных посредством Pydantic."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_user_crud():
    api = UserRequests(BASE_URL_PETSTORE)
    username = f"student_{uuid.uuid4().hex[:10]}"
    created = False

    user_data = User(
        id=10001,
        username=username,
        firstName="Ivan",
        lastName="Petrov",
        email="ivan.petrov@example.com",
        password="test_password_123",
        phone="79990000000",
        userStatus=1
    )

    try:
        with allure.step("Подготовка и генерация JSON пользователя"):
            json_data = user_data.model_dump(
                by_alias=True,
                exclude_none=True
            )
            allure.attach(
                user_data.model_dump_json(by_alias=True, indent=2),
                name="Данные нового пользователя",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("POST: создание пользователя"):
            create_result = api.create_user(json_data)
            allure.attach(
                str(create_result),
                name="Ответ создания пользователя"
            )
            assert create_result["code"] == 200
            created = True

        with allure.step("GET: получение и валидация пользователя"):
            response = api.get_user(username)
            user = User.model_validate(response)

            assert user.username == username
            assert user.first_name == "Ivan"

            allure.attach(
                user.model_dump_json(by_alias=True, indent=2),
                name="Полученный пользователь",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("PUT: обновление пользователя"):
            updated_data = user_data.model_copy(
                update={
                    "first_name": "Petr",
                    "email": "petr.petrov@example.com"
                }
            )

            api.update_user(
                username,
                updated_data.model_dump(
                    by_alias=True,
                    exclude_none=True
                )
            )

        with allure.step("GET: проверка обновлённых данных"):
            response = api.get_user(username)
            updated_user = User.model_validate(response)

            assert updated_user.first_name == "Petr"
            assert updated_user.email == "petr.petrov@example.com"

        with allure.step("DELETE: удаление пользователя"):
            delete_result = api.delete_user(username)
            assert delete_result["code"] == 200
            created = False

    finally:
        if created:
            api.delete_user(username)
        api.close()


@allure.epic("Petstore API")
@allure.feature("Store")
@allure.story("CRUD заказа")
@allure.title("Получение остатков и работа с заказом")
@allure.description(
    "Проверка получения инвентаря, создания, получения и удаления заказа "
    "с использованием Pydantic."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_store_crud():
    api = StoreRequests(BASE_URL_PETSTORE)
    order_id = uuid.uuid4().int % 1000000 or 1
    created = False

    order_data = Order(
        id=order_id,
        petId=1,
        quantity=2,
        shipDate="2026-11-19T12:00:00Z",
        status="placed",
        complete=True
    )

    try:
        with allure.step("GET: получение остатков товаров"):
            inventory = api.get_inventory()
            assert isinstance(inventory, dict)
            assert len(inventory) > 0

            allure.attach(
                str(inventory),
                name="Инвентарь магазина"
            )

        with allure.step("POST: создание заказа с JSON от Pydantic"):
            json_data = order_data.model_dump(
                by_alias=True,
                exclude_none=True,
                mode="json"
            )

            allure.attach(
                order_data.model_dump_json(by_alias=True, indent=2),
                name="JSON нового заказа",
                attachment_type=allure.attachment_type.JSON
            )

            created_order = api.create_order(json_data)
            assert created_order["id"] == order_id
            created = True

        with allure.step("GET: получение и валидация заказа"):
            response = api.get_order(order_id)
            order = Order.model_validate(response)

            assert order.id == order_id
            assert order.quantity == 2
            assert order.status == "placed"

            allure.attach(
                order.model_dump_json(by_alias=True, indent=2),
                name="Полученный заказ",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("DELETE: удаление заказа"):
            delete_result = api.delete_order(order_id)
            assert delete_result["code"] == 200
            created = False

    finally:
        if created:
            api.delete_order(order_id)
        api.close()


@allure.epic("Petstore API")
@allure.feature("Pydantic")
@allure.story("Валидация пользователя")
@allure.title("Отклонение некорректных данных пользователя")
def test_invalid_user_validation():
    with allure.step("Проверка отрицательного ID и пустого имени"):
        with pytest.raises(ValidationError):
            User(
                id=-1,
                username="",
                userStatus=-5
            )


@allure.epic("Petstore API")
@allure.feature("Pydantic")
@allure.story("Валидация заказа")
@allure.title("Отклонение некорректных данных заказа")
def test_invalid_order_validation():
    with allure.step("Проверка отрицательного количества товара"):
        with pytest.raises(ValidationError):
            Order(
                id=100,
                petId=1,
                quantity=-2,
                status="placed"
            )

    with allure.step("Проверка недопустимого статуса заказа"):
        with pytest.raises(ValidationError):
            Order(
                id=100,
                petId=1,
                quantity=2,
                status="unknown"
            )
