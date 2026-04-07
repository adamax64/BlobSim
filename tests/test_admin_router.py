import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app


class TestAdminRouter(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("controllers.admin_router.subprocess.run")
    @patch("controllers.admin_router.os.environ.get")
    def test_download_database_dump_success(self, mock_env_get, mock_subprocess_run):
        # Mock environment variables
        mock_env_get.side_effect = lambda key, default: {
            "POSTGRES_USER": "testuser",
            "POSTGRES_PASSWORD": "testpass",
            "POSTGRES_DB": "testdb",
            "POSTGRES_HOST": "localhost",
            "POSTGRES_PORT": "5432",
        }.get(key, default)

        # Mock subprocess.run
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "DUMP SQL CONTENT"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        # Mock auth - assume we have a way to get token, but for simplicity, patch require_auth
        with patch("controllers.admin_router.require_auth", return_value="Adamax"):
            response = self.client.get("/admin/db-dump")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/sql")
        self.assertIn(
            "attachment; filename=database_dump.sql",
            response.headers["content-disposition"],
        )
        self.assertEqual(response.text, "DUMP SQL CONTENT")

    @patch("controllers.admin_router.subprocess.run")
    @patch("controllers.admin_router.os.environ.get")
    def test_download_database_dump_failure(self, mock_env_get, mock_subprocess_run):
        # Mock environment variables
        mock_env_get.side_effect = lambda key, default: {
            "POSTGRES_USER": "testuser",
            "POSTGRES_PASSWORD": "testpass",
            "POSTGRES_DB": "testdb",
            "POSTGRES_HOST": "localhost",
            "POSTGRES_PORT": "5432",
        }.get(key, default)

        # Mock subprocess.run to fail
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "pg_dump error"
        mock_subprocess_run.return_value = mock_result

        with patch("controllers.admin_router.require_auth", return_value="Adamax"):
            response = self.client.get("/admin/db-dump")

        self.assertEqual(response.status_code, 500)
        self.assertIn("Database dump failed", response.json()["detail"])

    def test_download_database_dump_unauthorized(self):
        with patch("controllers.admin_router.require_auth", return_value="notadmin"):
            response = self.client.get("/admin/db-dump")

        self.assertEqual(response.status_code, 403)
        self.assertIn("Admin access required", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
