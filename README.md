# Практическая работа №1 — От требования к тестовому случаю и первому дефекту

Репозиторий содержит выполненную практическую работу по курсу IThub-24.3 на основе проекта Gilded Rose.

## Состав проекта

- `gilded_rose.py` — исходная реализация приложения.
- `tests/test_student_design.py` — разработанные автоматизированные тесты.
- `test_cases.md` — таблица тестовых случаев.
- `run.txt` — сведения об окружении и результаты запуска тестов.
- `defect.md` — описание обнаруженного дефекта DEF-001.
- `requirements.txt` — зависимости проекта.

## Исходный код

Использована зафиксированная версия исходного проекта Gilded Rose:

`d6407909c73b2ba61bfa7568af0d9bdce1902fd5`

## Требования

- Python 3.10 или новее.
- pytest 9.x.

## Установка и запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q tests/test_student_design.py
