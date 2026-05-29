import importlib
import sys
import unittest
from unittest.mock import MagicMock, patch

# Prevent domain imports that require database drivers during scheduler service tests.
sys.modules["cronjobs.progress_simulation"] = MagicMock(
    run_progress_simulation=MagicMock()
)
sys.modules["cronjobs.progress_competition"] = MagicMock(
    progress_competition=MagicMock()
)

scheduler_service = importlib.import_module("domain.scheduler_service")


class TestSchedulerService(unittest.TestCase):
    def tearDown(self):
        scheduler_service._scheduler_instance = None

    @patch("domain.scheduler_service.AsyncIOScheduler")
    def test_start_scheduler_creates_and_starts_scheduler(self, mock_scheduler_cls):
        mock_scheduler = MagicMock()
        mock_scheduler.running = False
        mock_scheduler_cls.return_value = mock_scheduler

        scheduler_service.start_scheduler()

        mock_scheduler_cls.assert_called_once()
        self.assertIs(scheduler_service.get_scheduler(), mock_scheduler)
        mock_scheduler.add_job.assert_called()
        mock_scheduler.start.assert_called_once()

    @patch("domain.scheduler_service.AsyncIOScheduler")
    def test_stop_scheduler_resets_scheduler_instance(self, mock_scheduler_cls):
        mock_scheduler = MagicMock()
        mock_scheduler.running = True
        scheduler_service._scheduler_instance = mock_scheduler

        scheduler_service.stop_scheduler()

        mock_scheduler.shutdown.assert_called_once_with(wait=False)
        self.assertIsNone(scheduler_service._scheduler_instance)

    @patch("domain.scheduler_service.AsyncIOScheduler")
    def test_restart_scheduler_after_stop_creates_new_instance(
        self, mock_scheduler_cls
    ):
        first_scheduler = MagicMock()
        first_scheduler.running = False
        second_scheduler = MagicMock()
        second_scheduler.running = False
        mock_scheduler_cls.side_effect = [first_scheduler, second_scheduler]

        scheduler_service.start_scheduler()
        self.assertIs(scheduler_service.get_scheduler(), first_scheduler)

        # Simulate shutdown and ensure the instance is cleared
        first_scheduler.running = True
        scheduler_service.stop_scheduler()
        self.assertIsNone(scheduler_service._scheduler_instance)

        scheduler_service.start_scheduler()
        self.assertIs(scheduler_service.get_scheduler(), second_scheduler)
        second_scheduler.start.assert_called_once()


if __name__ == "__main__":
    unittest.main()
