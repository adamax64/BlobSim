import unittest
from unittest.mock import MagicMock

from data.model.policy_type import PolicyType
from data.persistence.policy_repository import get_policy_by_type, get_active_policy_by_type
from data.persistence.policy_repository import upsert_policy


class TestPolicyRepository(unittest.TestCase):

    def test_get_policy_by_type_returns_any(self):
        session = MagicMock()
        expected = MagicMock()
        session.query.return_value.filter.return_value.first.return_value = expected

        res = get_policy_by_type(session, PolicyType.FACTORY_MODERNIZATION)
        self.assertIs(res, expected)

        # PolicyType only
        res2 = get_policy_by_type(session, PolicyType.FACTORY_MODERNIZATION)
        self.assertIs(res2, expected)

    def test_get_active_policy_by_type_normalizes(self):
        session = MagicMock()
        expected = MagicMock()
        session.query.return_value.filter.return_value.first.return_value = expected

        res = get_active_policy_by_type(session, PolicyType.GYM_IMPROVEMENT, 10)
        self.assertIs(res, expected)

    def test_upsert_create_when_none(self):
        session = MagicMock()
        mock_create = MagicMock()
        # patch create_policy import inside module
        import data.persistence.policy_repository as repo

        repo.get_policy_by_type = MagicMock(return_value=None)
        repo.create_policy = MagicMock(return_value=mock_create)

        res = upsert_policy(session, PolicyType.GYM_IMPROVEMENT, 150, 2)

        repo.create_policy.assert_called_once_with(session, PolicyType.GYM_IMPROVEMENT, 150, 2)
        self.assertIs(res, mock_create)

    def test_upsert_updates_existing(self):
        session = MagicMock()
        existing = MagicMock()
        existing.applied_level = 1
        existing.effect_until = 10

        import data.persistence.policy_repository as repo
        repo.get_policy_by_type = MagicMock(return_value=existing)

        res = upsert_policy(session, PolicyType.FACTORY_MODERNIZATION, 300, 5)

        self.assertEqual(existing.applied_level, 5)
        self.assertEqual(existing.effect_until, 300)
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(existing)
        self.assertIs(res, existing)


if __name__ == '__main__':
    unittest.main()
