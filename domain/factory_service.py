import random
from dataclasses import dataclass
from typing import Callable, Dict

from data.persistence.blob_repository import get_labouring_blob_count
from domain.enums.weather_type import WeatherTypeDto
from domain.utils.constants import (
    BASE_FACTORY_OUTPUT,
    HYDRO_MAX_OUTPUT,
    LABOUR_MAX_OUTPUT,
    SOLAR_MAX_OUTPUT,
    WIND_MAX_OUTPUT,
)


@dataclass(frozen=True)
class WeatherEffect:
    solar_ratio: float
    hydro_ratio: float
    wind_ratio: Callable[[float], float]


# How much of the maximum solar/hydro output each weather type yields, and how the
# raw random wind strength translates into wind turbine output for that weather.
WEATHER_EFFECTS: Dict[WeatherTypeDto, WeatherEffect] = {
    WeatherTypeDto.SUNNY: WeatherEffect(1.0, 0.25, lambda wind: wind * 0.5),
    WeatherTypeDto.SUNNY_CLOUDY: WeatherEffect(0.75, 0.30, lambda wind: wind),
    WeatherTypeDto.CLOUDY: WeatherEffect(0.50, 0.35, lambda wind: wind),
    WeatherTypeDto.SUNNY_RAIN: WeatherEffect(0.65, 0.85, lambda wind: wind),
    WeatherTypeDto.RAIN: WeatherEffect(0.40, 0.90, lambda wind: wind),
    WeatherTypeDto.HEAVY_RAIN: WeatherEffect(0.30, 1.00, lambda wind: wind),
    WeatherTypeDto.STORM: WeatherEffect(0.15, 1.00, lambda wind: 0.0),
    WeatherTypeDto.HEAT: WeatherEffect(1.00, 0.00, lambda wind: wind * 0.5),
    WeatherTypeDto.SNOWY: WeatherEffect(0.60, 0.05, lambda wind: wind),
    WeatherTypeDto.FREEZY: WeatherEffect(0.30, 0.00, lambda wind: wind * 0.5),
    WeatherTypeDto.FOGGY: WeatherEffect(0.40, 0.50, lambda wind: wind * 0.8),
}


def calculate_factory_output(weather: WeatherTypeDto, wind: float) -> int:
    """
    Calculate the factory's production output for one simulation tick: a constant base
    output plus independent solar, wind, hydro, and labour output chances.
    """

    effect = WEATHER_EFFECTS[weather]
    output = BASE_FACTORY_OUTPUT

    if random.random() < effect.solar_ratio:
        output += SOLAR_MAX_OUTPUT
    if random.random() < effect.wind_ratio(wind):
        output += WIND_MAX_OUTPUT
    if random.random() < effect.hydro_ratio:
        output += HYDRO_MAX_OUTPUT
    if random.random() < get_labour_output_chance():
        output += LABOUR_MAX_OUTPUT

    return output


def get_labour_output_chance() -> float:
    """Each blob currently doing labour adds one percentage point of output chance."""
    return min(get_labouring_blob_count() / 100, 1.0)


def get_output_chances(
    weather: WeatherTypeDto, wind: float
) -> tuple[float, float, float, float]:
    """
    Returns the (solar, wind, hydro, labour) chances of each source yielding one extra
    unit of factory output this tick, given the current weather and wind strength.
    """

    effect = WEATHER_EFFECTS[weather]
    return (
        effect.solar_ratio,
        effect.wind_ratio(wind),
        effect.hydro_ratio,
        get_labour_output_chance(),
    )
