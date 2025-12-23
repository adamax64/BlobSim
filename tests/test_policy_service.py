import unittest
from unittest.mock import MagicMock, patch

from data.model.policy_type import PolicyType
from domain.dtos.policy_dto import PolicyDto
from domain.policy_service import create_or_update_policy, fetch_active_policies


class TestPolicyService(unittest.TestCase):

    @patch('domain.policy_service.get_sim_time')
    @patch('domain.policy_service.upsert_policy')
    def test_create_new_policy_when_none(self, mock_create, mock_get_time):
        session = MagicMock()
        mock_get_time.return_value = 100
        create_or_update_policy(session, PolicyType.FACTORY_MODERNIZATION, 2)

        mock_create.assert_called_once()
        args = mock_create.call_args[0]
        # create_policy(session, policy_type_enum, effect_until, level)
        self.assertEqual(args[0], session)
        self.assertEqual(args[1], PolicyType.FACTORY_MODERNIZATION)
        # duration for level 2 is 6 -> effect_until = 100 + 6
        self.assertEqual(args[2], 106)
        self.assertEqual(args[3], 2)

    @patch('domain.policy_service.get_sim_time')
    @patch('domain.policy_service.get_active_policies')
    def test_fetch_maps_to_dto(self, mock_active, mock_get_time):
        session = MagicMock()
        mock_get_time.return_value = 10

        p = MagicMock()
        p.policy_type = PolicyType.FACTORY_MODERNIZATION.value
        p.effect_until = 20

        mock_active.return_value = [p]

        res = fetch_active_policies(session)

        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], PolicyDto)
        self.assertEqual(res[0].type, PolicyType.FACTORY_MODERNIZATION)


if __name__ == '__main__':
    unittest.main()
