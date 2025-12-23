import unittest
from unittest.mock import patch, MagicMock

from domain.blob_services.blob_update_service import update_all_blobs
from domain.enums.activity_type import ActivityType
from tests.utils import create_blob_model_mock


class TestBlobUpdateService(unittest.TestCase):

    @patch('domain.blob_services.blob_update_service.save_all_blobs')
    @patch('domain.blob_services.blob_update_service.get_all_blobs_by_name')
    @patch('domain.blob_services.blob_update_service.get_current_calendar')
    @patch('domain.blob_services.blob_update_service.get_event_next_day')
    @patch('domain.blob_services.blob_update_service.get_sim_time')
    @patch('domain.blob_services.blob_update_service.get_current_grandmaster_id')
    def test_mining_reward_distributed_to_single_random_miner(
        self,
        mock_get_sim_time,
        mock_get_event_next_day,
        mock_get_current_calendar,
        mock_get_current_grandmaster_id,
        mock_get_all_blobs_by_name,
        mock_save_all_blobs,
    ):
        # Create three blobs that choose mining
        b1 = create_blob_model_mock(id=1, money=0, current_activity=ActivityType.MINING)
        b2 = create_blob_model_mock(id=2, money=1, current_activity=ActivityType.MINING)
        b3 = create_blob_model_mock(id=3, money=2, current_activity=ActivityType.MINING)

        mock_get_all_blobs_by_name.return_value = [b1, b2, b3]
        mock_get_current_calendar.return_value = None
        mock_get_event_next_day.return_value = None
        mock_get_sim_time.return_value = 0
        mock_get_current_grandmaster_id.return_value = None

        session = MagicMock()

        # Force random.choice to pick b2 as the chosen miner
        with patch('random.choice', return_value=b2):
            update_all_blobs(session)

        # After update, b2 should receive reward equal to number of miners (3)
        self.assertEqual(b1.money, 0)
        self.assertEqual(b2.money, 1 + 3)
        self.assertEqual(b3.money, 2)

        # Ensure save_all_blobs was called at least once
        self.assertTrue(mock_save_all_blobs.called)


if __name__ == '__main__':
    unittest.main()
