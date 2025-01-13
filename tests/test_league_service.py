import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from data.model.result import Result
from data.model.event import Event
from domain.dtos.standings_dto import StandingsDTO
from domain.league_service import (
    get_all_real_leagues, _correct_contract_of_inactive_leagues,
    _promote_blobs_to_leagues, _create_new_league_if_necessary,
    _promote_dropout_winner_if_possibble, _get_dropout_winner, _demote_blobs_to_dropout,
    _get_free_spaces, _get_blobs_by_standings_order, _get_most_recent_standings, _retire_blobs
)
from domain.dtos.league_dto import LeagueDto
from data.model.league import League
from data.model.blob import Blob
from domain.utils.constants import MAX_FIELD_SIZE, QUEUE_LEVEL


def mock_blob(contract, league_id=None, integrity=1000, blob_id=0, born=0):
    return Blob(name="Test Blob", contract=contract, league_id=league_id, integrity=integrity, id=blob_id, born=born)


class TestLeagueService(unittest.TestCase):

    @patch('domain.league_service.league_repository.get_all_real_leagues')
    def test_get_all_real_leagues(self, mock_get_all_real_leagues):
        session = MagicMock(spec=Session)
        mock_leagues = [
            League(id=1, name='League 1', players=[Blob(), Blob()], level=1),
            League(id=2, name='League 2', players=[Blob(), Blob(), Blob()], level=2)
        ]
        mock_get_all_real_leagues.return_value = mock_leagues

        result = get_all_real_leagues(session)

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], LeagueDto)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].name, 'League 1')
        self.assertEqual(result[0].field_size, 2)
        self.assertEqual(result[0].level, 1)

    def test_correct_contract_of_inactive_leagues(self):
        session = MagicMock(spec=Session)
        league = League(id=1, name='League 1', players=[mock_blob(1), mock_blob(1)], level=1)
        leagues = [league]

        _correct_contract_of_inactive_leagues(session, leagues)

        for blob in league.players:
            self.assertEqual(blob.contract, 2)

    def test_promote_blobs_to_leagues(self):
        session = MagicMock(spec=Session)
        league1 = League(id=1, name='League 1', players=[mock_blob(1)], level=1)
        league2 = League(id=2, name='League 2', players=[mock_blob(1)], level=2)
        leagues = [league1, league2]

        _promote_blobs_to_leagues(session, leagues, 5)

        for blob in league2.players:
            self.assertEqual(blob.league_id, 1)

    @patch('domain.league_service.league_repository.save_league')
    def test_create_new_league_if_necessary(self, mock_save_league):
        session = MagicMock(spec=Session)
        league1 = League(id=1, name='League 1', players=[mock_blob(1)], level=1)
        queue = League(
            id=2, name='Queue',
            players=[mock_blob(1), mock_blob(2), mock_blob(1), mock_blob(2), mock_blob(1), mock_blob(2)],
            level=QUEUE_LEVEL
        )
        leagues = [league1, queue]

        _create_new_league_if_necessary(session, leagues, 5)

        mock_save_league.assert_called_once()
        args, _ = mock_save_league.call_args
        self.assertEqual(args[0], session)
        self.assertEqual(args[1].name, "League 2")
        self.assertEqual(args[1].level, 2)

    @patch('data.persistence.result_repository.get_most_recent_real_league_result_of_blob')
    @patch('domain.league_service.get_standings')
    def test_promote_dropout_winner_if_possibble(self, mock_get_standings, mock_get_blob_event):
        session = MagicMock(spec=Session)
        league1 = League(id=1, name='League 1', players=[mock_blob(6)], level=1)
        dropout_league = League(id=2, name='Dropout', players=[mock_blob(5, 2, blob_id=1)], level=0)
        leagues = [league1]

        mock_get_standings.return_value = [StandingsDTO(1, "Test Blob", False, [], 42)]
        mock_get_blob_event.return_value = Result(event=Event(league=league1))

        _promote_dropout_winner_if_possibble(session, leagues, dropout_league, 5)

        for blob in dropout_league.players:
            self.assertEqual(blob.league_id, 1)
            self.assertEqual(blob.contract, 8)

    @patch('domain.league_service.get_standings')
    def test_get_dropout_winner(self, mock_get_standings):
        session = MagicMock(spec=Session)
        dropout_league = League(id=1, name='Dropout', players=[mock_blob(1, blob_id=1)], level=0)

        mock_get_standings.return_value = [StandingsDTO(1, "Test Blob", False, [], 42)]

        result = _get_dropout_winner(session, dropout_league, 5)

        self.assertIsNotNone(result)

    def test_demote_blobs_to_dropout(self):
        session = MagicMock(spec=Session)
        league1 = League(id=1, name='League 1', players=[mock_blob(5)], level=1)
        dropout_league = League(id=2, name='Dropout', players=[], level=0)
        leagues = [league1]

        _demote_blobs_to_dropout(session, leagues, dropout_league, 5)

        for blob in league1.players:
            self.assertEqual(blob.league_id, 2)

    def test_get_free_spaces(self):
        league = League(id=1, name='League 1', players=[mock_blob(1)], level=1)

        result = _get_free_spaces(league)

        self.assertEqual(result, MAX_FIELD_SIZE - 1)

    @patch('domain.league_service.get_standings')
    def test_get_blobs_by_standings_order(self, mock_get_standings):
        session = MagicMock(spec=Session)
        league = League(id=1, name='League 1', players=[mock_blob(1)], level=1)
        mock_get_standings.return_value = []

        result = _get_blobs_by_standings_order(session, league, 5)

        self.assertEqual(len(result), 1)

    @patch('domain.league_service.get_standings')
    def test_get_most_recent_standings(self, mock_get_standings):
        session = MagicMock(spec=Session)
        league_id = 1

        def side_effect(league_id, season, session):
            if season == 5:
                return []
            elif season == 4:
                return [StandingsDTO(0, "Test Blob", False, [], 42)]
            return []

        mock_get_standings.side_effect = side_effect

        result = _get_most_recent_standings(session, league_id, 5)

        self.assertEqual(len(result), 1)
        self.assertEqual(mock_get_standings.call_count, 2)

    def test_retire_blobs(self):
        session = MagicMock(spec=Session)
        league = League(id=1, name='League 1', players=[mock_blob(5), mock_blob(7, integrity=10)], level=1)
        leagues = [league]

        _retire_blobs(session, leagues, 5)

        for blob in league.players:
            self.assertIsNone(blob.league_id)


if __name__ == '__main__':
    unittest.main()
