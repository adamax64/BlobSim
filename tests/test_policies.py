import unittest
from unittest.mock import patch, MagicMock

from domain.blob_services.blob_update_service import _proceed_with_activity
from domain.progression_service import progress_simulation
from domain.enums.activity_type import ActivityType
from data.model.blob import Blob
from data.model.sim_data import SimData


class TestPolicies(unittest.TestCase):

    @patch('domain.blob_services.blob_update_service.choose_random_policy_type')
    @patch('domain.blob_services.blob_update_service.get_sim_time')
    @patch('domain.blob_services.blob_update_service.create_or_update_policy')
    def test_grandmaster_policy_activity_creates_policy(self, mock_create, mock_get_time, mock_choice):
        session = MagicMock()
        mock_get_time.return_value = 100
        from data.model.policy_type import PolicyType
        mock_choice.return_value = PolicyType.FACTORY_MODERNIZATION

        blob = MagicMock(spec=Blob)
        blob.grandmasters = 2
        blob.current_activity = ActivityType.ADMINISTRATION

        _proceed_with_activity(blob, None, session)

        # duration for level 2 should be 6 days
        mock_create.assert_called_once()
        args = mock_create.call_args[0]
        self.assertEqual(args[0], session)
        self.assertEqual(args[1], PolicyType.FACTORY_MODERNIZATION)
        self.assertEqual(args[2], 2)  # level

    @patch('domain.blob_services.blob_update_service.get_sim_time')
    @patch('domain.blob_services.blob_update_service.get_active_policy_by_type')
    def test_gym_policy_increases_practice(self, mock_policy_query, mock_get_time):
        mock_get_time.return_value = 50
        gym_policy = MagicMock()
        gym_policy.applied_level = 2
        mock_policy_query.return_value = gym_policy

        session = MagicMock()
        blob = MagicMock(spec=Blob)
        blob.current_activity = ActivityType.PRACTICE

        multiplyer = _proceed_with_activity(blob, None, session)

        # practice effect base is PRACTICE_EFFECT (0.02) increased by 10% per level (2 -> +20%) = *1.2
        # resulting multiplyer components should be non-zero
        self.assertGreater(multiplyer.strength, 0)
        self.assertGreater(multiplyer.speed, 0)

    @patch('domain.blob_services.blob_creation_service.is_blob_created')
    @patch('domain.progression_service.get_active_policy_by_type')
    @patch('domain.progression_service.calculate_factory_output')
    @patch('domain.progression_service.choose_wind')
    @patch('domain.progression_service.choose_weather')
    @patch('domain.progression_service.get_sim_data')
    @patch('domain.progression_service.get_all_retired')
    def test_factory_and_pension_effects(
        self,
        mock_get_retired,
        mock_get_sim,
        mock_choose_weather,
        mock_choose_wind,
        mock_calculate_output,
        mock_policy_query,
        mock_is_blob_created,
    ):
        session = MagicMock()
        sim = SimData(id=1, sim_time=10, factory_progress=0)
        mock_get_sim.return_value = sim
        from domain.enums.weather_type import WeatherTypeDto
        mock_choose_weather.return_value = WeatherTypeDto.SUNNY
        mock_choose_wind.return_value = 0.4
        mock_calculate_output.return_value = 2

        # factory policy with applied_level 2
        factory_policy = MagicMock()
        factory_policy.applied_level = 2
        # pension policy applied_level 1
        pension_policy = MagicMock()
        pension_policy.applied_level = 1

        # when querying for FACTORY return [factory_policy], for PENSION return [pension_policy]
        from data.model.policy_type import PolicyType

        def policy_side_effect(session_arg, ptype, current_time):
            if ptype == PolicyType.FACTORY_MODERNIZATION:
                return factory_policy
            if ptype == PolicyType.PENSION_SCHEME:
                return pension_policy
            return None

        mock_policy_query.side_effect = policy_side_effect

        # retired blob
        retired = Blob(id=1, first_name='Old', last_name='Blob', money=0, terminated=5)
        mock_get_retired.return_value = [retired]
        mock_is_blob_created.return_value = False

        progress_simulation(session)

        # factory progress: calculate_factory_output mocked to 2, plus factory applied_level 2 = 4
        self.assertEqual(sim.factory_progress, 4)
        # retired blob should have received pension base coins = 1
        self.assertEqual(retired.money, 1)


if __name__ == '__main__':
    unittest.main()
