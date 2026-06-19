import unittest
from unittest.mock import MagicMock, patch

from data.model.item_type import ItemType
from data.model.state_type import StateType
from domain.item_service import grant_item_to_blob
from domain.utils.item_utils import DEFAULT_UNCONSUMABLE_DURABILITY
from tests.utils import create_blob_model_mock


def _item(item_id: int, item_type: ItemType, durability: int):
    item = MagicMock()
    item.id = item_id
    item.type = item_type
    item.durability = durability
    return item


def _state(state_id: int, state_type: StateType, effect_until: int):
    state = MagicMock()
    state.id = state_id
    state.type = state_type
    state.effect_until = effect_until
    return state


class TestItemService(unittest.TestCase):
    def test_coin_is_instantly_consumed_and_increases_money(self):
        blob = create_blob_model_mock(id=1, money=10)
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            grant_item_to_blob(blob, ItemType.COIN, session)

        self.assertEqual(blob.money, 11)
        mock_save_item.assert_not_called()

    def test_bag_of_money_is_instantly_consumed(self):
        blob = create_blob_model_mock(id=1, money=0)
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            grant_item_to_blob(blob, ItemType.BAG_OF_MONEY, session)

        self.assertEqual(blob.money, 5)
        mock_save_item.assert_not_called()

    def test_treasure_chest_is_instantly_consumed(self):
        blob = create_blob_model_mock(id=1, money=0)
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            grant_item_to_blob(blob, ItemType.TREASURE_CHEST, session)

        self.assertEqual(blob.money, 20)
        mock_save_item.assert_not_called()

    def test_maintenance_kit_is_instantly_consumed_and_increases_integrity(self):
        blob = create_blob_model_mock(id=1, integrity=10)
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            grant_item_to_blob(blob, ItemType.MAINTENANCE_KIT, session)

        self.assertEqual(blob.integrity, 13)
        mock_save_item.assert_not_called()

    @patch("domain.item_service.get_sim_time")
    @patch("domain.item_service.delete_state")
    def test_repair_kit_is_instantly_consumed_when_blob_is_injured(
        self, mock_delete_state, mock_get_sim_time
    ):
        mock_get_sim_time.return_value = 100
        injured_state = _state(7, StateType.INJURED, 120)
        blob = create_blob_model_mock(id=1)
        blob.states = [injured_state]
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            grant_item_to_blob(blob, ItemType.REPAIR_KIT, session)

        mock_delete_state.assert_called_once_with(session, 7)
        session.refresh.assert_called_once_with(blob)
        mock_save_item.assert_not_called()

    @patch("domain.item_service.get_sim_time")
    @patch("domain.item_service.get_items_of_blob")
    def test_repair_kit_is_saved_when_blob_is_not_injured(
        self, mock_get_items, mock_get_sim_time
    ):
        mock_get_sim_time.return_value = 100
        mock_get_items.return_value = []
        blob = create_blob_model_mock(id=1)
        blob.states = []
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            grant_item_to_blob(blob, ItemType.REPAIR_KIT, session)

        mock_save_item.assert_called_once()
        saved_item = mock_save_item.call_args[0][1]
        self.assertEqual(saved_item.type, ItemType.REPAIR_KIT)
        self.assertEqual(saved_item.durability, 1)

    @patch("domain.item_service.update_item")
    @patch("domain.item_service.get_items_of_blob")
    def test_energy_cell_resets_power_bank_durability(
        self, mock_get_items, mock_update_item
    ):
        power_bank = _item(1, ItemType.POWER_BANK, 1)
        mock_get_items.return_value = [power_bank]
        blob = create_blob_model_mock(id=1)
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            with patch("domain.item_service.random.choice", return_value=power_bank):
                grant_item_to_blob(blob, ItemType.ENERGY_CELL, session)

        self.assertEqual(power_bank.durability, DEFAULT_UNCONSUMABLE_DURABILITY)
        mock_update_item.assert_called_once_with(session, power_bank)
        mock_save_item.assert_not_called()

    @patch("domain.item_service.get_items_of_blob")
    def test_energy_cell_is_saved_without_rechargeable_item(self, mock_get_items):
        mock_get_items.return_value = []
        blob = create_blob_model_mock(id=1)
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            grant_item_to_blob(blob, ItemType.ENERGY_CELL, session)

        mock_save_item.assert_called_once()
        saved_item = mock_save_item.call_args[0][1]
        self.assertEqual(saved_item.type, ItemType.ENERGY_CELL)

    @patch("domain.item_service.get_items_of_blob")
    def test_non_instant_consumable_is_saved_to_inventory(self, mock_get_items):
        mock_get_items.return_value = []
        blob = create_blob_model_mock(id=1)
        session = MagicMock()

        with patch("domain.item_service.save_item") as mock_save_item:
            grant_item_to_blob(blob, ItemType.COOKIE, session)

        mock_save_item.assert_called_once()
        saved_item = mock_save_item.call_args[0][1]
        self.assertEqual(saved_item.type, ItemType.COOKIE)
        self.assertEqual(saved_item.durability, 1)

    @patch("domain.item_service.save_item")
    @patch("domain.item_service.delete_item")
    @patch("domain.item_service.get_items_of_blob")
    def test_sells_depleted_unconsumable_to_make_space(
        self, mock_get_items, mock_delete_item, mock_save_item
    ):
        depleted_cache = _item(1, ItemType.CACHE, 0)
        mock_get_items.return_value = [depleted_cache, _item(2, ItemType.COOKIE, 1), _item(3, ItemType.COOKIE, 1)]
        blob = create_blob_model_mock(id=1, money=0)
        session = MagicMock()

        grant_item_to_blob(blob, ItemType.REPAIR_KIT, session)

        mock_delete_item.assert_called_once_with(session, 1)
        self.assertEqual(blob.money, 5)
        mock_save_item.assert_called_once()

    @patch("domain.item_service.save_item")
    @patch("domain.item_service.delete_item")
    @patch("domain.item_service.get_items_of_blob")
    def test_sells_lower_rarity_item_to_make_space(
        self, mock_get_items, mock_delete_item, mock_save_item
    ):
        common_item = _item(1, ItemType.COOKIE, 1)
        mock_get_items.return_value = [
            common_item,
            _item(2, ItemType.POWER_BANK, 2),
            _item(3, ItemType.OVERCLOCKING_SCRIPT, 2),
        ]
        blob = create_blob_model_mock(id=1, money=0)
        session = MagicMock()

        grant_item_to_blob(blob, ItemType.REPAIR_KIT, session)

        mock_delete_item.assert_called_once_with(session, 1)
        self.assertEqual(blob.money, 1)
        mock_save_item.assert_called_once()

    @patch("domain.item_service.save_item")
    @patch("domain.item_service.delete_item")
    @patch("domain.item_service.get_items_of_blob")
    def test_sells_new_item_when_inventory_has_no_lower_rarity_items(
        self, mock_get_items, mock_delete_item, mock_save_item
    ):
        mock_get_items.return_value = [
            _item(1, ItemType.POWER_BANK, 2),
            _item(2, ItemType.OVERCLOCKING_SCRIPT, 2),
            _item(3, ItemType.PROCESSOR_PASTE, 10),
        ]
        blob = create_blob_model_mock(id=1, money=0)
        session = MagicMock()

        grant_item_to_blob(blob, ItemType.REPAIR_KIT, session)

        mock_delete_item.assert_not_called()
        mock_save_item.assert_not_called()
        self.assertEqual(blob.money, 10)

    @patch("domain.item_service.get_items_of_blob")
    def test_inventory_full_when_at_capacity(self, mock_get_items):
        mock_get_items.return_value = [
            _item(1, ItemType.COOKIE, 1),
            _item(2, ItemType.COOKIE, 1),
            _item(3, ItemType.COOKIE, 1),
        ]
        blob = create_blob_model_mock(id=1)
        session = MagicMock()

        from domain.item_service import is_inventory_full

        self.assertTrue(is_inventory_full(blob, session))


if __name__ == "__main__":
    unittest.main()
