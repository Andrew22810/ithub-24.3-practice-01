# КТ3_LXP — Тестирование Petstore API

## Описание

Проект демонстрирует работу с REST API учебного сервиса
[Swagger Petstore](https://petstore.swagger.io/).

Реализованы запросы для двух сущностей: `user` и `store`.
Для выполнения HTTP-запросов используется общий базовый класс `BaseRequest`.

Базовый URL API:

`https://petstore.swagger.io/v2`

## Структура проекта

- `base_request.py` — базовый класс для HTTP-запросов GET, POST, PUT и DELETE.
- `user_requests.py` — запросы для работы с пользователями.
- `store_requests.py` — запросы для работы с остатками товаров и заказами.
- `test_api.py` — автоматические интеграционные тесты.
- `requirements.txt` — зависимости проекта.

## Реализованные запросы

### User

| HTTP-метод | Endpoint | Назначение |
|---|---|---|
| POST | `/user` | Создание пользователя |
| GET | `/user/{username}` | Получение пользователя |
| PUT | `/user/{username}` | Обновление пользователя |
| DELETE | `/user/{username}` | Удаление пользователя |

### Store

| HTTP-метод | Endpoint | Назначение |
|---|---|---|
| GET | `/store/inventory` | Получение остатков товаров |
| POST | `/store/order` | Создание заказа |
| GET | `/store/order/{orderId}` | Получение заказа |
| DELETE | `/store/order/{orderId}` | Удаление заказа |

## Используемые технологии

- Python
- Requests
- Pytest
- REST API
- JSON

## Установка и запуск

Создание виртуального окружения:

```bash
python3 -m venv .venv
source .venv/bin/activate
