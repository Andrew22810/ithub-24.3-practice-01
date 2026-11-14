# Тестовые случаи — Gilded Rose

## Источник требований

[GildedRoseRequirements_ru.md](https://github.com/emilybache/GildedRose-Refactoring-Kata/blob/d6407909c73b2ba61bfa7568af0d9bdce1902fd5/GildedRoseRequirements_ru.md)

Одно обновление означает один вызов метода update_quality().

## Обозначения правил

- R1 — обычный товар теряет 1 единицу качества за день.
- R2 — после истечения срока обычный товар теряет качество вдвое быстрее.
- R3 — качество не может быть отрицательным.
- R4 — Aged Brie увеличивает качество на 1.
- R5 — качество не может превышать 50.
- R6 — Sulfuras не изменяет срок и качество.
- R7 — Backstage passes увеличивает качество на 1, 2 или 3 в зависимости от оставшегося срока.
- R8 — после концерта качество Backstage passes становится 0.
- R9 — Conjured теряет качество вдвое быстрее обычного товара.

## Таблица тестовых случаев

| ID | Правило | Начальное состояние | После одного обновления ожидается | Почему выбраны данные | Имя теста / результат |
|---|---|---|---|---|---|
| T01 | R1 | Item("ordinary", 5, 10) | sell_in=4, quality=9 | Обычный товар до истечения срока | test_ordinary_before_expiration — PASS |
| T02 | R1, R2 | Item("ordinary", 0, 10) | sell_in=-1, quality=8 | Граница истечения срока | test_ordinary_expiration_boundary — PASS |
| T03 | R1, R3 | Item("ordinary", 5, 0) | sell_in=4, quality=0 | Нижняя граница качества | test_ordinary_quality_cannot_be_negative — PASS |
| T04 | R4 | Item("Aged Brie", 5, 10) | sell_in=4, quality=11 | Проверка увеличения качества | test_aged_brie_increases_quality — PASS |
| T05 | R7 | Item("Backstage passes to a TAFKAL80ETC concert", 11, 20) | sell_in=10, quality=21 | Значение выше порога 10 | test_backstage_passes_thresholds (11) — PASS |
| T06 | R7 | Item("Backstage passes to a TAFKAL80ETC concert", 10, 20) | sell_in=9, quality=22 | Значение на пороге 10 | test_backstage_passes_thresholds (10) — PASS |
| T07 | R7 | Item("Backstage passes to a TAFKAL80ETC concert", 6, 20) | sell_in=5, quality=22 | Значение выше порога 5 | test_backstage_passes_thresholds (6) — PASS |
| T08 | R7 | Item("Backstage passes to a TAFKAL80ETC concert", 5, 20) | sell_in=4, quality=23 | Значение на пороге 5 | test_backstage_passes_thresholds (5) — PASS |
| T09 | R6 | Item("Sulfuras, Hand of Ragnaros", 0, 80) | sell_in=0, quality=80 | Легендарный товар | test_sulfuras_does_not_change — PASS |
| T10 | R9 | Item("Conjured Mana Cake", 5, 10) | sell_in=4, quality=8 | Двойное ухудшение качества | test_conjured_degrades_twice_as_fast — FAIL (DEF-001) |

| T11 | R4, R5 | Item("Aged Brie", 5, 50) | sell_in=4, quality=50 | Проверка верхней границы качества | test_aged_brie_quality_limit — PASS |

## Вывод

Набор включает обычные товары, специальные категории и граничные значения.

Проверяются переход через срок реализации (sell_in=0), пороги Backstage passes (11/10 и 6/5), а также нижняя граница качества (quality=0).

Ожидаемые значения рассчитаны по тексту требований, а не по результатам работы программы.

Результаты автоматизации будут добавлены после запуска тестов.
