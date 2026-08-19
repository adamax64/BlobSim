import unittest
from datetime import date, timedelta
from unittest.mock import patch, MagicMock

from domain.dtos.blob_dtos.blob_stats_dto import BlobStatsDto
from domain.dtos.sim_time_dto import SimTimeDto
from domain.mine_winners_service import (
    get_mine_winners,
    record_mine_winner,
    MINE_WINNERS_HISTORY_LIMIT,
)


def _blob_stats_dto(blob_id: int) -> BlobStatsDto:
    return BlobStatsDto(
        id=blob_id,
        name=f"Blob {blob_id}",
        born="1. 0 - 0",
        podiums=0,
        wins=0,
        championships=0,
        grandmasters=0,
        inventory=[],
        league_name=[],
        color="#888888",
        states=[],
        traits=[],
    )


class TestMineWinners(unittest.TestCase):

    @patch("domain.mine_winners_service.save_sim_data")
    @patch("domain.mine_winners_service.get_sim_data")
    def test_record_mine_winner_appends_entry(self, mock_get_sim_data, mock_save):
        sim_data = MagicMock()
        sim_data.mine_winners = []
        session = MagicMock()

        mock_get_sim_data.return_value = sim_data
        record_mine_winner(session, blob_id=7, amount=3)

        self.assertEqual(sim_data.mine_winners, [{"blob_id": 7, "amount": 3}])
        mock_save.assert_called_once_with(session, sim_data)

    @patch("domain.mine_winners_service.save_sim_data")
    @patch("domain.mine_winners_service.get_sim_data")
    def test_record_mine_winner_caps_history_at_limit(self, mock_get_sim_data, mock_save):
        sim_data = MagicMock()
        sim_data.mine_winners = [
            {"blob_id": i, "amount": i} for i in range(MINE_WINNERS_HISTORY_LIMIT)
        ]
        session = MagicMock()

        mock_get_sim_data.return_value = sim_data
        record_mine_winner(session, blob_id=99, amount=5)

        self.assertEqual(len(sim_data.mine_winners), MINE_WINNERS_HISTORY_LIMIT)
        # The oldest entry (blob_id 0) should have been popped, the new one appended last
        self.assertEqual(sim_data.mine_winners[0], {"blob_id": 1, "amount": 1})
        self.assertEqual(sim_data.mine_winners[-1], {"blob_id": 99, "amount": 5})

    @patch("domain.mine_winners_service.save_sim_data")
    @patch("domain.mine_winners_service.get_sim_data")
    def test_record_mine_winner_handles_none_existing_list(self, mock_get_sim_data, mock_save):
        sim_data = MagicMock()
        sim_data.mine_winners = None
        mock_get_sim_data.return_value = sim_data
        session = MagicMock()

        record_mine_winner(session, blob_id=1, amount=2)

        self.assertEqual(sim_data.mine_winners, [{"blob_id": 1, "amount": 2}])
        mock_save.assert_called_once_with(session, sim_data)

    @patch("domain.mine_winners_service.fetch_blob_by_id")
    @patch("domain.mine_winners_service.get_sim_data")
    def test_get_mine_winners_reverses_and_derives_dates(
        self, mock_get_sim_data, mock_fetch_blob
    ):
        # Stored oldest -> newest: blob 1 (1 day ago), blob 2 (today)
        mock_sim_data = MagicMock()
        mock_sim_data.mine_winners = [
            {"blob_id": 1, "amount": 2},
            {"blob_id": 2, "amount": 3},
        ]
        mock_sim_data.sim_time = 10
        mock_get_sim_data.return_value = mock_sim_data
        mock_fetch_blob.side_effect = lambda blob_id, session: _blob_stats_dto(blob_id)

        result = get_mine_winners(session=MagicMock())

        self.assertEqual(len(result.winners), 2)
        # Reversed: most recent (blob 2) first -> index 0 -> today
        self.assertEqual(result.winners[0].blob.id, 2)
        self.assertEqual(result.winners[0].amount, 3)
        self.assertEqual(result.winners[0].date, SimTimeDto(eon=0, season=1, epoch=2, cycle=1))
        # Second entry -> index 1 -> yesterday
        self.assertEqual(result.winners[1].blob.id, 1)
        self.assertEqual(result.winners[1].amount, 2)
        self.assertEqual(result.winners[1].date, SimTimeDto(eon=0, season=1, epoch=2, cycle=0))

    @patch("domain.mine_winners_service.fetch_blob_by_id")
    @patch("domain.mine_winners_service.get_sim_data")
    def test_get_mine_winners_empty(self, mock_get_sim_data, mock_fetch_blob):
        mock_sim_data = MagicMock()
        mock_sim_data.mine_winners = []
        mock_get_sim_data.return_value = mock_sim_data

        result = get_mine_winners(session=MagicMock())

        self.assertEqual(result.winners, [])
        mock_fetch_blob.assert_not_called()


if __name__ == "__main__":
    unittest.main()
