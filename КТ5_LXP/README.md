# КТ5 — Сложные тесты API

## Цель работы

Расширить тестирование Petstore API:
- подключить Allure для формирования наглядных отчётов о тестировании;
- использовать Pydantic для валидации данных;
- реализовать создание JSON на основе Pydantic-моделей;
- проверить корректность работы API пользователей и магазина.

API: https://petstore.swagger.io/

## Используемые технологии

- Python 3
- pytest
- requests
- Allure Pytest
- Allure Commandline
- Pydantic 2

## Структура проекта

- `base_request.py` — базовая логика HTTP-запросов.
- `user_requests.py` — запросы к API пользователей.
- `store_requests.py` — запросы к API магазина.
- `test_api.py` — API-тесты с Allure и Pydantic.
- `models.py` — Pydantic-модели User и Order.
- `check_models.py` — пример валидации данных и генерации JSON.
- `requirements.txt` — зависимости проекта.
- `pytest.ini` — настройки pytest.
- `.gitignore` — исключения для Git.

## Установка и настройка

Создать виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
