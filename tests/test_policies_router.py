import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app


class TestPoliciesRouter(unittest.TestCase):

    @patch('controllers.policies_router.fetch_active_policies')
    def test_get_active_policies_endpoint(self, mock_fetch):
        mock_fetch.return_value = []
        client = TestClient(app)
        resp = client.get('/policies/')
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
