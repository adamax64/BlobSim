import unittest
from unittest.mock import MagicMock

from data.model.item_type import ItemType
from domain.utils.item_utils import (
    DEFAULT_INVENTORY_SIZE,
    DEFAULT_UNCONSUMABLE_DURABILITY,
    EXTERNAL_STORAGE_INVENTORY_BONUS,
    INFINITE_DURABILITY,
    get_inventory_capacity,
    get_item_rarity,
    get_item_rarity_rank,
    get_item_sell_value,
    get_item_durability,
)


def _item(item_type: ItemType):
    item = MagicMock()
    item.type = item_type
    return item


class TestItemUtils(unittest.TestCase):
    def test_consumable_items_have_single_use_durability(self):
        self.assertEqual(get_item_durability(ItemType.COOKIE), 1)
        self.assertEqual(get_item_durability(ItemType.TREASURE_CHEST), 1)

    def test_default_unconsumable_items_have_durability_of_three(self):
        self.assertEqual(get_item_durability(ItemType.CACHE), DEFAULT_UNCONSUMABLE_DURABILITY)
        self.assertEqual(
            get_item_durability(ItemType.POWER_BANK), DEFAULT_UNCONSUMABLE_DURABILITY
        )
        self.assertEqual(
            get_item_durability(ItemType.OVERCLOCKING_DEVICE),
            DEFAULT_UNCONSUMABLE_DURABILITY,
        )

    def test_processor_paste_has_extended_durability(self):
        self.assertEqual(get_item_durability(ItemType.PROCESSOR_PASTE), 16)

    def test_external_storage_has_infinite_durability(self):
        self.assertEqual(
            get_item_durability(ItemType.EXTERNAL_STORAGE), INFINITE_DURABILITY
        )

    def test_default_inventory_capacity(self):
        self.assertEqual(get_inventory_capacity([]), DEFAULT_INVENTORY_SIZE)

    def test_external_storage_increases_inventory_capacity(self):
        items = [_item(ItemType.EXTERNAL_STORAGE), _item(ItemType.EXTERNAL_STORAGE)]
        self.assertEqual(
            get_inventory_capacity(items),
            DEFAULT_INVENTORY_SIZE + 2 * EXTERNAL_STORAGE_INVENTORY_BONUS,
        )

    def test_sell_values_match_rarity_money_items(self):
        self.assertEqual(get_item_sell_value(ItemType.COOKIE), 1)
        self.assertEqual(get_item_sell_value(ItemType.ENERGY_CELL), 5)
        self.assertEqual(get_item_sell_value(ItemType.SACK_OF_MONEY), 10)
        self.assertEqual(get_item_sell_value(ItemType.OVERCLOCKING_DEVICE), 20)

    def test_rarity_rank_order(self):
        self.assertLess(
            get_item_rarity_rank(ItemType.COIN),
            get_item_rarity_rank(ItemType.BAG_OF_MONEY),
        )
        self.assertLess(
            get_item_rarity_rank(ItemType.BAG_OF_MONEY),
            get_item_rarity_rank(ItemType.SACK_OF_MONEY),
        )
        self.assertLess(
            get_item_rarity_rank(ItemType.SACK_OF_MONEY),
            get_item_rarity_rank(ItemType.TREASURE_CHEST),
        )
        self.assertEqual(get_item_rarity(ItemType.CACHE), "rare")


if __name__ == "__main__":
    unittest.main()
