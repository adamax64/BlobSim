import unittest
from unittest.mock import MagicMock, patch

from data.model.item_type import ItemType
from data.model.state_type import StateType
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.sim_time_dto import SimTimeDto
from domain.dtos.state_dto import StateDto
from domain.item_service import apply_pre_event_items
from domain.utils.action_utils import (
    compute_item_min_score_boost,
    compute_item_skill_multiplier,
    get_random_coefficient,
)


def _item(item_id: int, item_type: ItemType, durability: int):
    item = MagicMock()
    item.id = item_id
    item.type = item_type
    item.durability = durability
    return item


def _state(state_type: StateType):
    return StateDto(
        type=state_type, effect_until=SimTimeDto(eon=0, season=1, epoch=1, cycle=2)
    )


class TestPreEventItems(unittest.TestCase):
    @patch("domain.item_service.create_state")
    @patch("domain.item_service._consume_item_after_use")
    @patch("domain.item_service.get_items_of_blob")
    @patch("domain.item_service.get_states_of_blob")
    @patch("domain.item_service.get_sim_time", return_value=100)
    def test_cookie_and_power_bank_create_item_states(
        self, mock_get_sim_time, mock_get_states_of_blob, mock_get_items, mock_consume, mock_create_state
    ):
        mock_get_items.return_value = [
            _item(1, ItemType.COOKIE, 1),
            _item(2, ItemType.POWER_BANK, 2),
        ]
        mock_get_states_of_blob.return_value = []
        session = MagicMock()

        apply_pre_event_items(1, session)

        mock_create_state.assert_any_call(
            session, 1, StateType.COOKIE_BOOST, 101
        )
        mock_create_state.assert_any_call(
            session, 1, StateType.POWER_BANK_BOOST, 101
        )
        self.assertEqual(mock_consume.call_count, 2)

    @patch("domain.item_service.create_state")
    @patch("domain.item_service._consume_item_after_use")
    @patch("domain.item_service.get_items_of_blob")
    @patch("domain.item_service.get_states_of_blob")
    @patch("domain.item_service.get_sim_time", return_value=100)
    def test_energy_cell_and_cache_create_min_score_states(
        self, mock_get_sim_time, mock_get_states_of_blob, mock_get_items, mock_consume, mock_create_state
    ):
        mock_get_items.return_value = [
            _item(1, ItemType.ENERGY_CELL, 1),
            _item(2, ItemType.CACHE, 2),
        ]
        mock_get_states_of_blob.return_value = []
        session = MagicMock()

        apply_pre_event_items(1, session)

        mock_create_state.assert_any_call(
            session, 1, StateType.ENERGY_CELL_BOOST, 101
        )
        mock_create_state.assert_any_call(session, 1, StateType.CACHE_BOOST, 101)

    @patch("domain.item_service.create_state")
    @patch("domain.item_service.get_items_of_blob")
    @patch("domain.item_service.get_states_of_blob")
    def test_unconsumable_with_zero_durability_is_not_used(
        self, mock_get_states_of_blob, mock_get_items, mock_create_state
    ):
        mock_get_items.return_value = [_item(1, ItemType.CACHE, 0)]
        mock_get_states_of_blob.return_value = []
        session = MagicMock()

        apply_pre_event_items(1, session)

        mock_create_state.assert_not_called()

    @patch("domain.item_service.create_state")
    @patch("domain.item_service.random.random", return_value=0.1)
    @patch("domain.item_service.get_sim_time", return_value=100)
    @patch("domain.item_service._consume_item_after_use")
    @patch("domain.item_service.get_items_of_blob")
    def test_depleted_overclock_can_be_used_and_risks_injury(
        self,
        mock_get_items,
        mock_consume,
        mock_get_sim_time,
        mock_random,
        mock_create_state,
    ):
        mock_get_items.return_value = [_item(1, ItemType.OVERCLOCKING_DEVICE, 0)]
        session = MagicMock()

        apply_pre_event_items(1, session)

        mock_create_state.assert_any_call(session, 1, StateType.INJURED, 104)
        mock_create_state.assert_any_call(
            session, 1, StateType.OVERCLOCKING_DEVICE_BOOST, 101
        )
        mock_consume.assert_called_once()

    def test_item_states_apply_skill_and_min_score_bonuses(self):
        contender = BlobCompetitorDto(
            id=1,
            name="Test Blob",
            strength=1.0,
            speed=1.0,
            color="#000000",
            states=[
                _state(StateType.COOKIE_BOOST),
                _state(StateType.POWER_BANK_BOOST),
                _state(StateType.ENERGY_CELL_BOOST),
            ],
        )

        self.assertAlmostEqual(compute_item_skill_multiplier(contender, 0), 1.06)
        self.assertAlmostEqual(compute_item_min_score_boost(contender, 0), 0.15)

    def test_min_score_boost_raises_random_coefficient_floor(self):
        samples = [get_random_coefficient(False, 0.05) for _ in range(100)]
        self.assertTrue(all(sample >= 0.05 for sample in samples))


if __name__ == "__main__":
    unittest.main()
