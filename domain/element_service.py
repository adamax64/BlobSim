import random

from data.model.sim_data import SimData
from domain.enums.element_dto import ElementDto
from domain.enums.weather_type import WeatherTypeDto
from domain.weather_service import WEATHER_EFFECTS


def generate_daily_element_tokens(sim_data: SimData) -> None:
    """
    Roll today's element token gains based on the current weather/wind, mutating `sim_data`
    in place. Should be called once per simulation day, after `sim_data.weather`/`sim_data.wind`
    have been rolled for the day.
    """
    weather_effect = WEATHER_EFFECTS.get(sim_data.weather)

    if weather_effect and random.random() < weather_effect.solar_ratio:
        sim_data.fire_tokens = (sim_data.fire_tokens or 0) + 1
    if sim_data.weather == WeatherTypeDto.HEAT:
        sim_data.fire_tokens = (sim_data.fire_tokens or 0) + 1

    if weather_effect and random.random() < weather_effect.hydro_ratio:
        sim_data.water_tokens = (sim_data.water_tokens or 0) + 1
    if sim_data.weather == WeatherTypeDto.HEAVY_RAIN:
        sim_data.water_tokens = (sim_data.water_tokens or 0) + 1

    if random.random() < (sim_data.wind or 0.0):
        sim_data.wind_tokens = (sim_data.wind_tokens or 0) + 1

    if sim_data.weather == WeatherTypeDto.SNOWY:
        sim_data.ice_tokens = (sim_data.ice_tokens or 0) + 1
    elif sim_data.weather == WeatherTypeDto.FREEZY:
        sim_data.ice_tokens = (sim_data.ice_tokens or 0) + 2

    if sim_data.weather == WeatherTypeDto.FOGGY:
        sim_data.beast_tokens = (sim_data.beast_tokens or 0) + 1

    sim_data.neutral_tokens = (sim_data.neutral_tokens or 0) + 1


def pick_element_for_new_blob(sim_data: SimData) -> ElementDto:
    """
    Pick an element for a newly created blob, weighted by the accumulated daily element
    tokens, then reset all token counters back to 0. A `neutral` token contributes towards
    `ElementDto.NONE` (no element).
    """
    weights = {
        ElementDto.FIRE: sim_data.fire_tokens or 0,
        ElementDto.WIND: sim_data.wind_tokens or 0,
        ElementDto.WATER: sim_data.water_tokens or 0,
        ElementDto.ICE: sim_data.ice_tokens or 0,
        ElementDto.BEAST: sim_data.beast_tokens or 0,
        ElementDto.NONE: sim_data.neutral_tokens or 0,
    }

    sim_data.fire_tokens = 0
    sim_data.wind_tokens = 0
    sim_data.water_tokens = 0
    sim_data.ice_tokens = 0
    sim_data.beast_tokens = 0
    sim_data.neutral_tokens = 0

    total_weight = sum(weights.values())
    if total_weight <= 0:
        return ElementDto.NONE

    elements, element_weights = zip(*weights.items())
    return random.choices(elements, weights=element_weights, k=1)[0]
