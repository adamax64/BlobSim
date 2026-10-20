import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from controllers.auth_router import get_current_user
from domain.dtos.league_dto import LeagueDto
from domain.dtos.translations_dto import TranslationsDto
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
            return "Redacted"

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
            return "Redacted"

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

    @patch("controllers.admin_router.update_league_names")
    def test_update_league_names_success(self, mock_update_league_names):
        async def mock_get_current_user():
            return "Redacted"

        app.dependency_overrides[get_current_user] = mock_get_current_user
        mock_update_league_names.return_value = [
            LeagueDto(
                id=1,
                name=[
                    TranslationsDto(language="en", text="Top League"),
                    TranslationsDto(language="hu", text="Csúcs Liga"),
                ],
                field_size=8,
                level=1,
            )
        ]

        payload = [
            {
                "id": 1,
                "name": [
                    {"language": "en", "text": "Top League"},
                    {"language": "hu", "text": "Csúcs Liga"},
                ],
            }
        ]
        response = self.client.post("/admin/leagues/names", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["name"][0]["text"], "Top League")
        mock_update_league_names.assert_called_once()

    def test_update_league_names_unauthorized(self):
        response = self.client.post(
            "/admin/leagues/names",
            json=[
                {
                    "id": 1,
                    "name": [
                        {"language": "en", "text": "Top League"},
                        {"language": "hu", "text": "Csúcs Liga"},
                    ],
                }
            ],
        )

        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
