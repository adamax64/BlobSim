import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from data.model.blob import Blob
from data.model.event import Event
from data.model.result import Result
from domain.dtos.standings_dtos.standings_dto import StandingsDTO
from domain.standings_service import (
    get_standings,
    get_standings_snippet_by_blob,
    invalidate_standings_cache,
)


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


class TestStandingsSnippetByBlobEventAware(unittest.TestCase):
    def setUp(self):
        invalidate_standings_cache()

    def tearDown(self):
        invalidate_standings_cache()

    @patch("domain.standings_service.get_standings")
    @patch("domain.standings_service.get_event_by_id")
    @patch("domain.standings_service.get_blob_by_id")
    def test_with_event_id_uses_event_season_and_round(
        self, mock_get_blob, mock_get_event, mock_get_standings
    ):
        blob = MagicMock()
        blob.league = MagicMock(id=9)
        mock_get_blob.return_value = blob

        event = MagicMock()
        event.season = 4
        event.round = 6
        event.league_id = 9
        mock_get_event.return_value = event

        standing_above = StandingsDTO(
            blob_id=10, name="A", color="red", is_contract_ending=False, is_rookie=False,
            results=[], num_of_rounds=8, total_points=5,
        )
        standing_self = StandingsDTO(
            blob_id=1, name="Me", color="blue", is_contract_ending=False, is_rookie=False,
            results=[], num_of_rounds=8, total_points=3,
        )
        standing_below = StandingsDTO(
            blob_id=11, name="B", color="green", is_contract_ending=False, is_rookie=False,
            results=[], num_of_rounds=8, total_points=1,
        )
        mock_get_standings.return_value = [standing_above, standing_self, standing_below]

        session = MagicMock(spec=Session)
        result = get_standings_snippet_by_blob(1, session, event_id=99)

        mock_get_event.assert_called_once_with(session, 99)
        mock_get_standings.assert_called_once_with(9, 4, 4, session, through_round=5)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].blob_id, 1)

    @patch("domain.standings_service.get_sim_time", return_value=123)
    @patch("domain.standings_service.get_season", return_value=8)
    @patch("domain.standings_service.get_standings")
    @patch("domain.standings_service.get_event_by_id")
    @patch("domain.standings_service.get_blob_by_id")
    def test_without_event_id_uses_current_season_and_no_truncation(
        self, mock_get_blob, mock_get_event, mock_get_standings, _mock_get_season, _mock_get_sim_time
    ):
        blob = MagicMock()
        blob.league = MagicMock(id=9)
        mock_get_blob.return_value = blob
        mock_get_standings.return_value = []

        session = MagicMock(spec=Session)
        get_standings_snippet_by_blob(1, session)

        mock_get_event.assert_not_called()
        mock_get_standings.assert_called_once_with(9, 8, 8, session, through_round=None)


if __name__ == "__main__":
    unittest.main()
