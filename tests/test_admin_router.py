import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from controllers.auth_router import get_current_user
from main import app


POSTGRES_ENV = {
    "POSTGRES_USER": "testuser",
    "POSTGRES_PASSWORD": "testpass",
    "POSTGRES_DB": "testdb",
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": "5432",
}


def _mock_env_get(key, default=None):
    return POSTGRES_ENV.get(key, default)


class TestAdminRouter(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    @patch("controllers.admin_router.find_pg_dump", return_value="/usr/bin/pg_dump")
    @patch("controllers.admin_router.subprocess.run")
    @patch("controllers.admin_router.os.environ.get", side_effect=_mock_env_get)
    def test_download_database_dump_success(
        self, _mock_env_get, mock_subprocess_run, _mock_find_pg_dump
    ):
        async def mock_get_current_user():
            return "Adamax"

        app.dependency_overrides[get_current_user] = mock_get_current_user

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "DUMP SQL CONTENT"
        mock_result.stderr = ""
        mock_subprocess_run.return_value = mock_result

        response = self.client.get("/admin/db-dump")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/sql")
        self.assertRegex(
            response.headers["content-disposition"],
            r"attachment; filename=bcs_dump_\d{8}\.sql",
        )
        self.assertEqual(response.text, "DUMP SQL CONTENT")

    @patch("controllers.admin_router.find_pg_dump", return_value="/usr/bin/pg_dump")
    @patch("controllers.admin_router.subprocess.run")
    @patch("controllers.admin_router.os.environ.get", side_effect=_mock_env_get)
    def test_download_database_dump_failure(
        self, _mock_env_get, mock_subprocess_run, _mock_find_pg_dump
    ):
        async def mock_get_current_user():
            return "Adamax"

        app.dependency_overrides[get_current_user] = mock_get_current_user

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "pg_dump error"
        mock_subprocess_run.return_value = mock_result

        response = self.client.get("/admin/db-dump")

        self.assertEqual(response.status_code, 500)
        self.assertIn("Database dump failed", response.json()["detail"])

    def test_download_database_dump_unauthorized(self):
        response = self.client.get("/admin/db-dump")

        self.assertEqual(response.status_code, 401)
        self.assertIn("Not authenticated", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
