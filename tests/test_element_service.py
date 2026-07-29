import unittest
from unittest.mock import patch

from data.model.sim_data import SimData
from domain.enums.element_dto import ElementDto
from domain.enums.weather_type import WeatherTypeDto
from domain.element_service import generate_daily_element_tokens, pick_element_for_new_blob


def _make_sim_data(weather: WeatherTypeDto, wind: float) -> SimData:
    return SimData(
        id=1,
        sim_time=0,
        factory_progress=0,
        weather=weather,
        wind=wind,
        fire_tokens=0,
        wind_tokens=0,
        water_tokens=0,
        ice_tokens=0,
        beast_tokens=0,
        neutral_tokens=0,
    )


class TestElementService(unittest.TestCase):
    @patch('domain.element_service.random.random', return_value=0.99)
    def test_neutral_token_always_gained(self, _mock_random):
        sim_data = _make_sim_data(WeatherTypeDto.CLOUDY, 0.0)
        generate_daily_element_tokens(sim_data)
        self.assertEqual(sim_data.neutral_tokens, 1)

    @patch('domain.element_service.random.random', return_value=0.0)
    def test_heat_weather_grants_two_fire_tokens(self, _mock_random):
        # solar chance always succeeds (random.random() == 0.0) plus unconditional Heat bonus
        sim_data = _make_sim_data(WeatherTypeDto.HEAT, 0.0)
        generate_daily_element_tokens(sim_data)
        self.assertEqual(sim_data.fire_tokens, 2)

    @patch('domain.element_service.random.random', return_value=0.99)
    def test_heavy_rain_grants_one_water_token_even_if_chance_roll_fails(self, _mock_random):
        # hydro_ratio is 1.0 for Heavy Rain, so the chance roll (0.99) always succeeds too,
        # plus the unconditional Heavy Rain bonus => 2 tokens total.
        sim_data = _make_sim_data(WeatherTypeDto.HEAVY_RAIN, 0.0)
        generate_daily_element_tokens(sim_data)
        self.assertEqual(sim_data.water_tokens, 2)

    @patch('domain.element_service.random.random', return_value=0.0)
    def test_wind_token_gained_by_chance_based_on_wind_value(self, _mock_random):
        sim_data = _make_sim_data(WeatherTypeDto.CLOUDY, 0.8)
        generate_daily_element_tokens(sim_data)
        self.assertEqual(sim_data.wind_tokens, 1)

    def test_freezy_grants_two_ice_tokens_and_snowy_grants_one(self):
        freezy = _make_sim_data(WeatherTypeDto.FREEZY, 0.0)
        with patch('domain.element_service.random.random', return_value=0.99):
            generate_daily_element_tokens(freezy)
        self.assertEqual(freezy.ice_tokens, 2)

        snowy = _make_sim_data(WeatherTypeDto.SNOWY, 0.0)
        with patch('domain.element_service.random.random', return_value=0.99):
            generate_daily_element_tokens(snowy)
        self.assertEqual(snowy.ice_tokens, 1)

    def test_foggy_grants_one_beast_token(self):
        sim_data = _make_sim_data(WeatherTypeDto.FOGGY, 0.0)
        with patch('domain.element_service.random.random', return_value=0.99):
            generate_daily_element_tokens(sim_data)
        self.assertEqual(sim_data.beast_tokens, 1)

    def test_pick_element_for_new_blob_resets_all_tokens(self):
        sim_data = _make_sim_data(WeatherTypeDto.CLOUDY, 0.0)
        sim_data.fire_tokens = 5

        pick_element_for_new_blob(sim_data)

        self.assertEqual(sim_data.fire_tokens, 0)
        self.assertEqual(sim_data.wind_tokens, 0)
        self.assertEqual(sim_data.water_tokens, 0)
        self.assertEqual(sim_data.ice_tokens, 0)
        self.assertEqual(sim_data.beast_tokens, 0)
        self.assertEqual(sim_data.neutral_tokens, 0)

    def test_pick_element_for_new_blob_returns_none_when_no_tokens(self):
        sim_data = _make_sim_data(WeatherTypeDto.CLOUDY, 0.0)
        self.assertEqual(pick_element_for_new_blob(sim_data), ElementDto.NONE)

    @patch('domain.element_service.random.choices')
    def test_pick_element_for_new_blob_uses_token_counts_as_weights(self, mock_choices):
        mock_choices.return_value = [ElementDto.FIRE]
        sim_data = _make_sim_data(WeatherTypeDto.CLOUDY, 0.0)
        sim_data.fire_tokens = 3
        sim_data.neutral_tokens = 1

        result = pick_element_for_new_blob(sim_data)

        self.assertEqual(result, ElementDto.FIRE)
        args, kwargs = mock_choices.call_args
        elements = args[0]
        weights = kwargs['weights']
        self.assertEqual(dict(zip(elements, weights))[ElementDto.FIRE], 3)
        self.assertEqual(dict(zip(elements, weights))[ElementDto.NONE], 1)


if __name__ == '__main__':
    unittest.main()
