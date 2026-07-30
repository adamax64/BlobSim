import unittest

from domain.enums.element_dto import ElementDto
from domain.enums.season_temperature import SeasonTemperatureDto
from domain.enums.weather_type import WeatherTypeDto
from domain.utils.element_utils import (
    ELEMENT_WEATHER_MODIFIERS,
    compute_element_skill_multipliers,
    compute_wind_buff,
)


class TestElementUtils(unittest.TestCase):
    def test_no_element_gives_no_bonus_in_neutral_weather(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.NONE, WeatherTypeDto.CLOUDY, 0.5, SeasonTemperatureDto.WARM
        )
        self.assertEqual((strength_mult, speed_mult), (1.0, 1.0))

    def test_no_element_gives_no_bonus_with_no_weather(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.NONE, None, 0.5, SeasonTemperatureDto.WARM
        )
        self.assertEqual((strength_mult, speed_mult), (1.0, 1.0))

    def test_none_element_arg_gives_no_bonus_in_neutral_weather(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            None, WeatherTypeDto.CLOUDY, 0.5, SeasonTemperatureDto.WARM
        )
        self.assertEqual((strength_mult, speed_mult), (1.0, 1.0))

    def test_no_element_rain_penalizes_speed_only(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.NONE, WeatherTypeDto.RAIN, 0.5, SeasonTemperatureDto.WARM
        )
        self.assertAlmostEqual(strength_mult, 1.0)
        self.assertAlmostEqual(speed_mult, 0.99)

    def test_no_element_heavy_rain_penalizes_speed_only(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.NONE, WeatherTypeDto.HEAVY_RAIN, 0.5, SeasonTemperatureDto.WARM
        )
        self.assertAlmostEqual(strength_mult, 1.0)
        self.assertAlmostEqual(speed_mult, 0.98)

    def test_no_element_heat_penalizes_speed_and_strength(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.NONE, WeatherTypeDto.HEAT, 0.5, SeasonTemperatureDto.WARM
        )
        self.assertAlmostEqual(strength_mult, 0.98)
        self.assertAlmostEqual(speed_mult, 0.98)

    def test_no_element_freezy_penalizes_speed_and_strength(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.NONE, WeatherTypeDto.FREEZY, 0.5, SeasonTemperatureDto.WARM
        )
        self.assertAlmostEqual(strength_mult, 0.98)
        self.assertAlmostEqual(speed_mult, 0.98)

    def test_fire_applies_weather_table_and_non_cold_season_bonus(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.FIRE, WeatherTypeDto.HEAT, 0.5, SeasonTemperatureDto.WARM
        )
        # +10% weather bonus (Heat) + 2% further strength modifier (non-cold season)
        self.assertAlmostEqual(strength_mult, 1.12)
        self.assertAlmostEqual(speed_mult, 1.10)

    def test_fire_loses_further_strength_bonus_in_cold_season(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.FIRE, WeatherTypeDto.HEAT, 0.5, SeasonTemperatureDto.COLD
        )
        self.assertAlmostEqual(strength_mult, 1.10)
        self.assertAlmostEqual(speed_mult, 1.10)

    def test_water_applies_weather_table_uniformly(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.WATER, WeatherTypeDto.HEAVY_RAIN, 0.5, SeasonTemperatureDto.NEUTRAL
        )
        self.assertAlmostEqual(strength_mult, 1.10)
        self.assertAlmostEqual(speed_mult, 1.10)

    def test_ice_bonuses_in_cold_season(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.ICE, WeatherTypeDto.CLOUDY, 0.5, SeasonTemperatureDto.COLD
        )
        # 0% weather (cloudy) + 1% strength (cold) ; speed always +1%
        self.assertAlmostEqual(strength_mult, 1.01)
        self.assertAlmostEqual(speed_mult, 1.01)

    def test_ice_penalizes_strength_in_neutral_and_warm_season(self):
        for season in (SeasonTemperatureDto.NEUTRAL, SeasonTemperatureDto.WARM):
            strength_mult, speed_mult = compute_element_skill_multipliers(
                ElementDto.ICE, WeatherTypeDto.CLOUDY, 0.5, season
            )
            self.assertAlmostEqual(strength_mult, 0.99)
            self.assertAlmostEqual(speed_mult, 1.01)

    def test_beast_gets_flat_strength_and_speed_bonus_on_top_of_weather_table(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.BEAST, WeatherTypeDto.FOGGY, 0.5, SeasonTemperatureDto.NEUTRAL
        )
        # +4% weather (Foggy) + 2% flat bonus, for both strength and speed
        self.assertAlmostEqual(strength_mult, 1.06)
        self.assertAlmostEqual(speed_mult, 1.06)

    def test_wind_buff_is_linear_between_minus_5_and_plus_5_percent(self):
        self.assertAlmostEqual(compute_wind_buff(0.0), -0.05)
        self.assertAlmostEqual(compute_wind_buff(0.5), 0.0)
        self.assertAlmostEqual(compute_wind_buff(1.0), 0.05)

    def test_wind_element_uses_wind_value_instead_of_weather_table(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.WIND, WeatherTypeDto.STORM, 1.0, SeasonTemperatureDto.NEUTRAL
        )
        # +5% wind buff on both stats, plus a further +2% speed bonus (not foggy)
        self.assertAlmostEqual(strength_mult, 1.05)
        self.assertAlmostEqual(speed_mult, 1.07)

    def test_wind_element_loses_further_speed_bonus_in_foggy_weather(self):
        strength_mult, speed_mult = compute_element_skill_multipliers(
            ElementDto.WIND, WeatherTypeDto.FOGGY, 1.0, SeasonTemperatureDto.NEUTRAL
        )
        self.assertAlmostEqual(strength_mult, 1.05)
        self.assertAlmostEqual(speed_mult, 1.05)

    def test_element_weather_modifiers_cover_all_weather_types_for_each_element(self):
        for element in (ElementDto.FIRE, ElementDto.WATER, ElementDto.ICE, ElementDto.BEAST):
            self.assertEqual(set(ELEMENT_WEATHER_MODIFIERS[element].keys()), set(WeatherTypeDto))


if __name__ == '__main__':
    unittest.main()
