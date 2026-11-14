import pytest

from gilded_rose import GildedRose, Item


def update_item(item):
    """Выполняет одно обновление товара."""
    GildedRose([item]).update_quality()
    return item


def test_ordinary_before_expiration():
    item = update_item(Item("ordinary", 5, 10))

    assert item.sell_in == 4
    assert item.quality == 9


def test_ordinary_expiration_boundary():
    item = update_item(Item("ordinary", 0, 10))

    assert item.sell_in == -1
    assert item.quality == 8


def test_ordinary_quality_cannot_be_negative():
    item = update_item(Item("ordinary", 5, 0))

    assert item.sell_in == 4
    assert item.quality == 0


def test_aged_brie_increases_quality():
    item = update_item(Item("Aged Brie", 5, 10))

    assert item.sell_in == 4
    assert item.quality == 11


def test_aged_brie_quality_limit():
    item = update_item(Item("Aged Brie", 5, 50))

    assert item.sell_in == 4
    assert item.quality == 50


@pytest.mark.parametrize(
    "initial_sell_in, expected_quality",
    [
        (11, 21),
        (10, 22),
        (6, 22),
        (5, 23),
    ],
)
def test_backstage_passes_thresholds(initial_sell_in, expected_quality):
    item = update_item(
        Item(
            "Backstage passes to a TAFKAL80ETC concert",
            initial_sell_in,
            20,
        )
    )

    assert item.sell_in == initial_sell_in - 1
    assert item.quality == expected_quality


def test_sulfuras_does_not_change():
    item = update_item(
        Item("Sulfuras, Hand of Ragnaros", 0, 80)
    )

    assert item.sell_in == 0
    assert item.quality == 80


def test_conjured_degrades_twice_as_fast():
    item = update_item(Item("Conjured Mana Cake", 5, 10))

    assert item.sell_in == 4
    assert item.quality == 8
