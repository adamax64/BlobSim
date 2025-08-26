import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

from domain.calendar_service import (
  recreate_calendar_for_next_season,
  get_season_calendar,
  conclude_calendar_event
)


class TestCalendarService(unittest.TestCase):

    @patch('domain.calendar_service.save_all_calendar_records')
    @patch('domain.calendar_service.get_epoch_cycle_by_level')
    @patch('domain.calendar_service.get_number_of_rounds_by_size')
    @patch('domain.calendar_service.get_all_real_leagues')
    @patch('domain.calendar_service.clear_calendar')
    def test_recreate_calendar_for_next_season(self, mock_clear, mock_get_leagues, mock_get_rounds, mock_get_cycle, mock_save_all):
        session = MagicMock(spec=Session)
        # Mock league
        league = MagicMock()
        league.id = 1
        league.level = 2
        league.players = [1, 2, 3, 4]
        mock_get_leagues.return_value = [league]
        mock_get_cycle.return_value = 99
        mock_get_rounds.return_value = 10  # >= MINIMAL_SEASON
        # Patch _create_calendar_record to return a simple object
        with patch('domain.calendar_service._create_calendar_record', side_effect=lambda *a, **kw: MagicMock(date=a[1])) as mock_create:
            recreate_calendar_for_next_season(session, 42)
            mock_clear.assert_called_once_with(session)
            mock_get_leagues.assert_called_once_with(session)
            mock_save_all.assert_called_once()
            self.assertTrue(mock_create.called)

    @patch('domain.calendar_service.convert_to_sim_time')
    @patch('domain.calendar_service.get_sim_data')
    @patch('domain.calendar_service.get_calendar')
    def test_get_season_calendar(self, mock_get_calendar, mock_get_sim_data, mock_convert):
        session = MagicMock(spec=Session)
        # Mock calendar event
        event = MagicMock()
        event.date = 123
        event.league.name = 'Test League'
        event.league.level = 1
        event.concluded = False
        event.event_type = 'SOME_EVENT'
        mock_get_calendar.return_value = {1: event}
        mock_get_sim_data.return_value.sim_time = 123
        mock_convert.return_value = 'SIM_TIME_DTO'
        result = get_season_calendar(session)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, 'SIM_TIME_DTO')
        self.assertEqual(result[0].league_name, 'Test League')
        self.assertEqual(result[0].league_level, 1)
        self.assertEqual(result[0].is_current, True)

    @patch('domain.calendar_service.save_calendar_event')
    @patch('domain.calendar_service.get_next_unconcluded')
    def test_conclude_calendar_event(self, mock_get_next, mock_save):
        session = MagicMock(spec=Session)
        calendar = MagicMock()
        calendar.concluded = False
        mock_get_next.return_value = calendar
        conclude_calendar_event(session)
        self.assertTrue(calendar.concluded)
        mock_save.assert_called_once_with(session, calendar)

    @patch('domain.calendar_service.get_next_unconcluded')
    def test_conclude_calendar_event_already_concluded(self, mock_get_next):
        session = MagicMock(spec=Session)
        calendar = MagicMock()
        calendar.concluded = True
        mock_get_next.return_value = calendar
        with self.assertRaises(Exception):
            conclude_calendar_event(session)

    if __name__ == '__main__':
        unittest.main()
