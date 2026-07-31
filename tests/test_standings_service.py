import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from data.model.blob import Blob
from data.model.event import Event
from data.model.result import Result
from domain.standings_service import get_standings, invalidate_standings_cache


def _mock_result(blob, date, position, points):
    result = Result(blob=blob, event=Event(date=date), position=position, points=points)
    return result


class TestStandingsServiceThroughRound(unittest.TestCase):
    def setUp(self):
        invalidate_standings_cache()

        self.blob_a = Blob(id=1, first_name="A", last_name="Blob", color="red")
        self.blob_b = Blob(id=2, first_name="B", last_name="Blob", color="blue")

        # Blob A: leads after round 1, but Blob B overtakes by round 2.
        self.results = [
            _mock_result(self.blob_a, date=1, position=1, points=10),
            _mock_result(self.blob_b, date=1, position=2, points=5),
            _mock_result(self.blob_a, date=2, position=2, points=5),
            _mock_result(self.blob_b, date=2, position=1, points=10),
        ]

    def tearDown(self):
        invalidate_standings_cache()

    @patch("domain.standings_service.get_number_of_rounds_by_size", return_value=2)
    @patch("domain.standings_service.get_results_of_league_by_season")
    def test_through_round_truncates_results_and_recomputes_points(
        self, mock_get_results, _mock_num_rounds
    ):
        mock_get_results.return_value = self.results
        session = MagicMock(spec=Session)

        standings = get_standings(1, 1, 1, session, through_round=1)

        self.assertEqual(len(standings), 2)
        for standing in standings:
            self.assertEqual(len(standing.results), 1)
        self.assertEqual(standings[0].blob_id, self.blob_a.id)
        self.assertEqual(standings[0].total_points, 10)
        self.assertEqual(standings[1].blob_id, self.blob_b.id)
        self.assertEqual(standings[1].total_points, 5)

    @patch("domain.standings_service.get_number_of_rounds_by_size", return_value=2)
    @patch("domain.standings_service.get_results_of_league_by_season")
    def test_through_round_none_returns_full_standings(
        self, mock_get_results, _mock_num_rounds
    ):
        mock_get_results.return_value = self.results
        session = MagicMock(spec=Session)

        standings = get_standings(1, 1, 1, session)

        self.assertEqual(len(standings), 2)
        for standing in standings:
            self.assertEqual(len(standing.results), 2)
        self.assertEqual(standings[0].blob_id, self.blob_a.id)
        self.assertEqual(standings[0].total_points, 15)
        self.assertEqual(standings[1].blob_id, self.blob_b.id)
        self.assertEqual(standings[1].total_points, 15)

    @patch("domain.standings_service.get_number_of_rounds_by_size", return_value=2)
    @patch("domain.standings_service.get_results_of_league_by_season")
    def test_through_round_does_not_mutate_cached_full_standings(
        self, mock_get_results, _mock_num_rounds
    ):
        mock_get_results.return_value = self.results
        session = MagicMock(spec=Session)

        get_standings(1, 1, 1, session, through_round=1)
        full_standings = get_standings(1, 1, 1, session)

        self.assertEqual(mock_get_results.call_count, 1)
        for standing in full_standings:
            self.assertEqual(len(standing.results), 2)

    @patch("domain.standings_service.get_number_of_rounds_by_size", return_value=2)
    @patch("domain.standings_service.get_results_of_league_by_season")
    def test_through_round_beyond_available_rounds_keeps_full_results(
        self, mock_get_results, _mock_num_rounds
    ):
        mock_get_results.return_value = self.results
        session = MagicMock(spec=Session)

        standings = get_standings(1, 1, 1, session, through_round=5)

        for standing in standings:
            self.assertEqual(len(standing.results), 2)


if __name__ == "__main__":
    unittest.main()
