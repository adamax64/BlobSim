import unittest
from unittest.mock import patch

from domain.enums.weather_type import WeatherTypeDto
from domain.factory_service import calculate_factory_output, get_output_chances


class TestFactoryService(unittest.TestCase):
    def setUp(self):
        self.labour_count_patcher = patch(
            "domain.factory_service.get_labouring_blob_count", return_value=0
        )
        self.labour_count_patcher.start()

    def tearDown(self):
        self.labour_count_patcher.stop()

    @patch("domain.factory_service.random.random")
    def test_calculate_factory_output_all_chances_hit(self, mock_random):
        # solar_ratio=1.0 (SUNNY), wind_ratio=0.4*0.5=0.2, hydro_ratio=0.25;
        # rolls just below each threshold so all three weather bonuses trigger
        mock_random.side_effect = [0.0, 0.1, 0.24, 0.0]

        self.assertEqual(calculate_factory_output(WeatherTypeDto.SUNNY, 0.4), 4)

    @patch("domain.factory_service.random.random")
    def test_calculate_factory_output_all_chances_missed(self, mock_random):
        # FOGGY with no wind: solar_ratio=0.4, wind_ratio=max(0, 0-0.2)=0, hydro_ratio=0.5;
        # rolls above the solar/hydro thresholds miss, and the wind ratio of 0 always misses
        mock_random.side_effect = [0.99, 0.5, 0.99, 0.5]

        self.assertEqual(calculate_factory_output(WeatherTypeDto.FOGGY, 0.0), 1)

    @patch("domain.factory_service.random.random")
    def test_calculate_factory_output_storm_ignores_wind(self, mock_random):
        # storm's wind_ratio is always 0, so the wind roll can never succeed
        mock_random.side_effect = [0.0, 0.0, 0.0, 0.5]

        self.assertEqual(calculate_factory_output(WeatherTypeDto.STORM, 0.9), 3)

    @patch("domain.factory_service.random.random")
    def test_calculate_factory_output_heat_reduces_wind_by_half(self, mock_random):
        # HEAT: solar_ratio=1.0 (always hits), hydro_ratio=0.0 (always misses),
        # wind_ratio = max(0, wind - 0.5) = 0.3; roll below that triggers the wind bonus
        mock_random.side_effect = [0.0, 0.29, 0.5, 0.5]

        self.assertEqual(calculate_factory_output(WeatherTypeDto.HEAT, 0.8), 3)

    @patch("domain.factory_service.random.random")
    @patch("domain.factory_service.get_labouring_blob_count", return_value=50)
    def test_labouring_blobs_add_one_percent_chance_each(
        self, mock_labour_count, _mock_random
    ):
        # Storm always yields hydro output; the 50% labour chance also hits at 0.49.
        _mock_random.side_effect = [0.49, 0.49, 0.49, 0.49]
        self.assertEqual(calculate_factory_output(WeatherTypeDto.STORM, 0.9), 3)
        mock_labour_count.assert_called_once_with()

    @patch("domain.factory_service.get_labouring_blob_count", return_value=150)
    def test_labour_output_chance_is_capped_at_one(self, mock_labour_count):
        self.assertEqual(
            get_output_chances(WeatherTypeDto.STORM, 0.9),
            (0.15, 0.0, 1.0, 1.0),
        )
        mock_labour_count.assert_called_once_with()

    @patch("domain.factory_service.get_labouring_blob_count", return_value=25)
    def test_get_output_chances_includes_labour_probability(self, mock_labour_count):
        self.assertEqual(
            get_output_chances(WeatherTypeDto.SUNNY, 0.4),
            (1.0, 0.2, 0.25, 0.25),
        )
        mock_labour_count.assert_called_once_with()
