import unittest
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from domain.blob_services.blob_fetching_service import fetch_blob_by_id


class TestFetchBlobByIdEventAware(unittest.TestCase):
    def _mock_blob(self, league_id=5):
        blob = MagicMock()
        blob.league = MagicMock(id=league_id)
        return blob

    @patch("domain.blob_services.blob_fetching_service.map_to_blob_state_dto")
    @patch("domain.blob_services.blob_fetching_service.get_current_grandmaster_id", return_value=None)
    @patch("domain.blob_services.blob_fetching_service.get_standings")
    @patch("domain.blob_services.blob_fetching_service.get_event_by_id")
    @patch("domain.blob_services.blob_fetching_service.get_blob_by_id")
    @patch("domain.blob_services.blob_fetching_service.get_season", return_value=7)
    def test_with_event_id_uses_event_season_and_round(
        self,
        _mock_get_season,
        mock_get_blob,
        mock_get_event,
        mock_get_standings,
        _mock_gm_id,
        mock_map_dto,
    ):
        blob = self._mock_blob()
        mock_get_blob.return_value = blob

        event = MagicMock()
        event.season = 3
        event.round = 2
        event.league_id = 5
        mock_get_event.return_value = event

        standing = MagicMock()
        standing.blob_id = 1
        mock_get_standings.return_value = [standing]

        session = MagicMock(spec=Session)

        fetch_blob_by_id(1, session, event_id=42)

        mock_get_event.assert_called_once_with(session, 42)
        mock_get_standings.assert_called_once_with(
            session=session, league_id=5, season=3, current_season=3, through_round=1
        )
        _, kwargs = mock_map_dto.call_args
        self.assertEqual(kwargs["standings_position"], 1)
        self.assertIsNone(kwargs["last_season_standings_position"])

    @patch("domain.blob_services.blob_fetching_service.map_to_blob_state_dto")
    @patch("domain.blob_services.blob_fetching_service.get_current_grandmaster_id", return_value=None)
    @patch("domain.blob_services.blob_fetching_service.get_last_season_standings_position", return_value=None)
    @patch("domain.blob_services.blob_fetching_service.get_standings")
    @patch("domain.blob_services.blob_fetching_service.get_event_by_id")
    @patch("domain.blob_services.blob_fetching_service.get_blob_by_id")
    @patch("domain.blob_services.blob_fetching_service.get_season", return_value=7)
    def test_without_event_id_uses_current_season_and_no_truncation(
        self,
        _mock_get_season,
        mock_get_blob,
        mock_get_event,
        mock_get_standings,
        _mock_last_season_position,
        _mock_gm_id,
        _mock_map_dto,
    ):
        blob = self._mock_blob()
        mock_get_blob.return_value = blob
        mock_get_standings.return_value = []

        session = MagicMock(spec=Session)

        fetch_blob_by_id(1, session)

        mock_get_event.assert_not_called()
        mock_get_standings.assert_called_once_with(
            session=session, league_id=5, season=7, current_season=7, through_round=None
        )


if __name__ == "__main__":
    unittest.main()
