import unittest
from unittest.mock import patch

from domain.enums.season_temperature import SeasonTemperatureDto
from domain.enums.weather_type import WeatherTypeDto
from domain.weather_service import (
    WEATHER_EFFECTS,
    WEATHER_RARITY,
    choose_weather,
    choose_wind,
    get_next_season_temperature,
)


class TestWeatherService(unittest.TestCase):
    def test_weather_rarity_covers_all_weather_types_for_each_season_temperature(self):
        for season_temperature in SeasonTemperatureDto:
            self.assertEqual(
                set(WEATHER_RARITY[season_temperature].keys()), set(WeatherTypeDto)
            )

    def test_weather_effects_cover_all_weather_types(self):
        self.assertEqual(set(WEATHER_EFFECTS.keys()), set(WeatherTypeDto))

    @patch("domain.weather_service.random.choices")
    def test_choose_weather_uses_rarity_weights_for_season_temperature(
        self, mock_choices
    ):
        mock_choices.return_value = [WeatherTypeDto.SUNNY]

        result = choose_weather(SeasonTemperatureDto.COLD)

        self.assertEqual(result, WeatherTypeDto.SUNNY)
        args, kwargs = mock_choices.call_args
        self.assertEqual(
            args[0], list(WEATHER_RARITY[SeasonTemperatureDto.COLD].keys())
        )
        self.assertEqual(
            kwargs["weights"], list(WEATHER_RARITY[SeasonTemperatureDto.COLD].values())
        )

    @patch("domain.weather_service.random.random")
    def test_choose_wind_returns_random_value(self, mock_random):
        mock_random.return_value = 0.42

        self.assertEqual(choose_wind(), 0.42)

    @patch("domain.weather_service.random.random")
    def test_get_next_season_temperature_stays_when_roll_below_half(self, mock_random):
        mock_random.return_value = 0.49

        self.assertEqual(
            get_next_season_temperature(SeasonTemperatureDto.NEUTRAL),
            SeasonTemperatureDto.NEUTRAL,
        )

    @patch("domain.weather_service.random.random")
    def test_get_next_season_temperature_rises_when_cold(self, mock_random):
        mock_random.return_value = 0.5

        self.assertEqual(
            get_next_season_temperature(SeasonTemperatureDto.COLD),
            SeasonTemperatureDto.NEUTRAL,
        )

    @patch("domain.weather_service.random.random")
    def test_get_next_season_temperature_drops_when_warm(self, mock_random):
        mock_random.return_value = 0.5

        self.assertEqual(
            get_next_season_temperature(SeasonTemperatureDto.WARM),
            SeasonTemperatureDto.NEUTRAL,
        )

    @patch("domain.weather_service.random.choice")
    @patch("domain.weather_service.random.random")
    def test_get_next_season_temperature_neutral_shifts_up_or_down(
        self, mock_random, mock_choice
    ):
        mock_random.return_value = 0.5

        mock_choice.return_value = SeasonTemperatureDto.WARM
        self.assertEqual(
            get_next_season_temperature(SeasonTemperatureDto.NEUTRAL),
            SeasonTemperatureDto.WARM,
        )

        mock_choice.return_value = SeasonTemperatureDto.COLD
        self.assertEqual(
            get_next_season_temperature(SeasonTemperatureDto.NEUTRAL),
            SeasonTemperatureDto.COLD,
        )


if __name__ == "__main__":
    unittest.main()
