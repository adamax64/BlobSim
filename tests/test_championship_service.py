import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from domain.championship_service import end_eon_if_over, end_season_if_over
from domain.dtos.league_dto import LeagueDto
from domain.dtos.grandmaster_standings_dto import GrandmasterStandingsDTO
from domain.dtos.standings_dto import StandingsDTO
from data.model.blob import Blob
from domain.utils.blob_name_utils import format_blob_name
from domain.utils.constants import GRANDMASTER_PRIZE, CHAMPION_PRIZE, CYCLES_PER_EON, ROOKIE_OF_THE_YEAR_PRIZE


class TestChampionshipService(unittest.TestCase):

    @patch('domain.championship_service.count_unconcluded_for_league')
    @patch('domain.championship_service.get_grandmaster_standings')
    @patch('domain.championship_service.get_blob_by_id')
    @patch('domain.championship_service.save_blob')
    def test_end_eon_if_over(self, mock_save_blob, mock_get_blob_by_id, mock_get_grandmaster_standings, mock_count_unconcluded):
        session = MagicMock(spec=Session)
        league = LeagueDto(id=1, name='League 1', field_size=5, level=1)
        season = 4

        mock_count_unconcluded.return_value = 0
        mock_get_grandmaster_standings.return_value = [
            GrandmasterStandingsDTO(blob_id=1, name="Test Blob", color="#FFFFFF", championships=3, gold=5, silver=4, bronze=3, points=100),
            GrandmasterStandingsDTO(blob_id=2, name="Blob Doe", color="#000000", championships=1, gold=5, silver=4, bronze=3, points=100),
            ]
        mock_blob = Blob(id=1, first_name="Test", last_name="Blob", grandmasters=0, money=0, contract=0, integrity=0)
        mock_get_blob_by_id.return_value = mock_blob

        result = end_eon_if_over(season, league, session)

        self.assertIsNotNone(result)
        self.assertEqual(mock_blob.grandmasters, 1)
        self.assertEqual(mock_blob.money, GRANDMASTER_PRIZE)
        self.assertEqual(mock_blob.contract, 1)
        self.assertEqual(mock_blob.integrity, CYCLES_PER_EON)
        mock_save_blob.assert_called_once_with(session, mock_blob)

    @patch('domain.championship_service.add_season_ended_news')
    @patch('domain.championship_service.add_rookie_of_the_year_news')
    @patch('domain.championship_service.count_unconcluded_for_league')
    @patch('domain.championship_service.get_standings')
    @patch('domain.championship_service.get_all_by_league_order_by_id')
    @patch('domain.championship_service.save_all_blobs')
    def test_end_season_if_over(
        self,
        mock_save_all_blobs,
        mock_get_all_by_league_order_by_id,
        mock_get_standings,
        mock_count_unconcluded,
        mock_add_rookie_of_the_year_news,
        mock_add_season_ended_news
    ):
        session = MagicMock(spec=Session)
        mock_standings = [
            StandingsDTO(
                blob_id=1,
                name="Blob 1",
                color="#111111",
                is_contract_ending=False,
                is_rookie=False,
                results=[],
                num_of_rounds=10,
                total_points=100
            ),
            StandingsDTO(
                blob_id=2,
                name="Blob 2",
                color="#222222",
                is_contract_ending=False,
                is_rookie=False,
                results=[],
                num_of_rounds=10,
                total_points=90
            ),
            StandingsDTO(
                blob_id=3,
                name="Blob 3",
                color="#333333",
                is_contract_ending=False,
                is_rookie=False,
                results=[],
                num_of_rounds=10,
                total_points=80
            ),
            StandingsDTO(
                blob_id=4,
                name="Blob 4",
                color="#444444",
                is_contract_ending=False,
                is_rookie=False,
                results=[],
                num_of_rounds=10,
                total_points=70
            ),
            StandingsDTO(
                blob_id=5,
                name="Blob 5",
                color="#555555",
                is_contract_ending=False,
                is_rookie=False,
                results=[],
                num_of_rounds=10,
                total_points=60
            ),
            StandingsDTO(
                blob_id=6,
                name="Blob 6",
                color="#666666",
                is_contract_ending=False,
                is_rookie=False,
                results=[],
                num_of_rounds=10,
                total_points=50
            )
        ]
        mock_get_standings.return_value = mock_standings

        def run_test_for_level(level):
            mock_blobs = {
                1: Blob(id=1, first_name="Blob", last_name="1", contract=0, championships=0, season_victories=0, money=0),
                2: Blob(id=2, first_name="Blob", last_name="2", contract=0, championships=0, season_victories=0, money=0),
                3: Blob(id=3, first_name="Blob", last_name="3", contract=0, championships=0, season_victories=0, money=0),
                4: Blob(id=4, first_name="Blob", last_name="4", contract=0, championships=0, season_victories=0, money=0, debut=1),
                5: Blob(id=5, first_name="Blob", last_name="5", contract=0, championships=0, season_victories=0, money=0, debut=1),
                6: Blob(id=6, first_name="Blob", last_name="6", contract=0, championships=0, season_victories=0, money=0, debut=1)
            }
            mock_get_all_by_league_order_by_id.return_value = mock_blobs

            league = LeagueDto(id=level, name=f'League {level}', field_size=2, level=level)
            season = 1

            mock_count_unconcluded.return_value = 0

            result = end_season_if_over(league, season, session)

            self.assertIsNotNone(result)
            self.assertEqual(mock_blobs[1].contract, 2)
            self.assertEqual(mock_blobs[1].championships, 1 if level == 1 else 0)
            self.assertEqual(mock_blobs[1].season_victories, 1 if level > 1 else 0)
            self.assertEqual(mock_blobs[1].money, CHAMPION_PRIZE)
            self.assertEqual(mock_blobs[2].contract, 1)
            self.assertEqual(mock_blobs[2].championships, 0)
            self.assertEqual(mock_blobs[2].season_victories, 0)
            self.assertEqual(mock_blobs[2].money, 0)
            self.assertEqual(mock_blobs[4].contract, 1)
            self.assertEqual(mock_blobs[4].championships, 0)
            self.assertEqual(mock_blobs[4].season_victories, 0)
            self.assertEqual(mock_blobs[4].money, ROOKIE_OF_THE_YEAR_PRIZE)
            mock_save_all_blobs.assert_called_with(session, list(mock_blobs.values()))
            mock_add_rookie_of_the_year_news.assert_called_with(format_blob_name(mock_blobs[4]), session)
            mock_add_season_ended_news.assert_called_with(league.name, format_blob_name(mock_blobs[1]), session)

        run_test_for_level(1)
        run_test_for_level(2)


if __name__ == '__main__':
    unittest.main()
