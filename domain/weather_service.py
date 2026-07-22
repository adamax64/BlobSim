import random
from dataclasses import dataclass
from typing import Callable, Dict, List

from domain.enums.weather_type import WeatherTypeDto
from domain.enums.season_temperature import SeasonTemperatureDto
from domain.utils.constants import (
    BASE_FACTORY_OUTPUT,
    SOLAR_MAX_OUTPUT,
    WIND_MAX_OUTPUT,
    HYDRO_MAX_OUTPUT,
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
    WeatherTypeDto.HEAT: WeatherEffect(1.00, 0.00, lambda wind: max(0.0, wind - 0.5)),
    WeatherTypeDto.SNOWY: WeatherEffect(0.60, 0.05, lambda wind: wind),
    WeatherTypeDto.FREEZY: WeatherEffect(0.30, 0.00, lambda wind: max(0.0, wind - 0.5)),
    WeatherTypeDto.FOGGY: WeatherEffect(0.40, 0.50, lambda wind: max(0.0, wind - 0.2)),
}


# Relative rarity weights of each weather type depending on the current season temperature.
WEATHER_RARITY: Dict[SeasonTemperatureDto, Dict[WeatherTypeDto, float]] = {
    SeasonTemperatureDto.COLD: {
        WeatherTypeDto.SUNNY: 0.1,
        WeatherTypeDto.SUNNY_CLOUDY: 0.5,
        WeatherTypeDto.CLOUDY: 1,
        WeatherTypeDto.SUNNY_RAIN: 0.01,
        WeatherTypeDto.RAIN: 0.2,
        WeatherTypeDto.HEAVY_RAIN: 0.1,
        WeatherTypeDto.STORM: 0.1,
        WeatherTypeDto.HEAT: 0,
        WeatherTypeDto.SNOWY: 1,
        WeatherTypeDto.FREEZY: 1,
        WeatherTypeDto.FOGGY: 0.6,
    },
    SeasonTemperatureDto.NEUTRAL: {
        WeatherTypeDto.SUNNY: 1,
        WeatherTypeDto.SUNNY_CLOUDY: 1,
        WeatherTypeDto.CLOUDY: 1,
        WeatherTypeDto.SUNNY_RAIN: 1,
        WeatherTypeDto.RAIN: 1,
        WeatherTypeDto.HEAVY_RAIN: 1,
        WeatherTypeDto.STORM: 1,
        WeatherTypeDto.HEAT: 0,
        WeatherTypeDto.SNOWY: 0,
        WeatherTypeDto.FREEZY: 0,
        WeatherTypeDto.FOGGY: 1,
    },
    SeasonTemperatureDto.WARM: {
        WeatherTypeDto.SUNNY: 1.5,
        WeatherTypeDto.SUNNY_CLOUDY: 0.5,
        WeatherTypeDto.CLOUDY: 0.4,
        WeatherTypeDto.SUNNY_RAIN: 0.5,
        WeatherTypeDto.RAIN: 0.1,
        WeatherTypeDto.HEAVY_RAIN: 0.05,
        WeatherTypeDto.STORM: 0.05,
        WeatherTypeDto.HEAT: 1,
        WeatherTypeDto.SNOWY: 0,
        WeatherTypeDto.FREEZY: 0,
        WeatherTypeDto.FOGGY: 0,
    },
}


_SEASON_TEMPERATURE_STAGES: List[SeasonTemperatureDto] = [
    SeasonTemperatureDto.COLD,
    SeasonTemperatureDto.NEUTRAL,
    SeasonTemperatureDto.WARM,
]


def choose_weather(season_temperature: SeasonTemperatureDto) -> WeatherTypeDto:
    """ Randomly pick a weather type, weighted by rarity for the given season temperature """

    rarity = WEATHER_RARITY[season_temperature]
    weather_types = list(rarity.keys())
    weights = list(rarity.values())
    return random.choices(weather_types, weights=weights, k=1)[0]


def choose_wind() -> float:
    """ Randomly pick a wind strength between 0 and 1 """

    return random.random()


def get_next_season_temperature(current: SeasonTemperatureDto) -> SeasonTemperatureDto:
    """
    On season change, there is a 50% chance the temperature stays the same. Otherwise it
    shifts by one stage: up if currently COLD, down if currently WARM, and 50-50 up or down
    if currently NEUTRAL.
    """

    if random.random() < 0.5:
        return current

    if current == SeasonTemperatureDto.COLD or current == SeasonTemperatureDto.WARM:
        return SeasonTemperatureDto.NEUTRAL
    else:
        return random.choice([SeasonTemperatureDto.COLD, SeasonTemperatureDto.WARM])


def calculate_factory_output(weather: WeatherTypeDto, wind: float) -> int:
    """
    Calculate the factory's production output for one simulation tick, split into 4 parts:
    a constant base output, plus solar, wind turbine and hydro turbine outputs which each
    have an independent chance (depending on weather and, for wind, wind strength) of
    yielding one extra unit of output.
    """

    effect = WEATHER_EFFECTS[weather]
    output = BASE_FACTORY_OUTPUT

    if random.random() < effect.solar_ratio:
        output += SOLAR_MAX_OUTPUT
    if random.random() < effect.wind_ratio(wind):
        output += WIND_MAX_OUTPUT
    if random.random() < effect.hydro_ratio:
        output += HYDRO_MAX_OUTPUT

    return output


def get_output_chances(weather: WeatherTypeDto, wind: float) -> tuple[float, float, float]:
    """
    Returns the (solar, wind, hydro) chances that each corresponding turbine yields one
    extra unit of factory output this tick, given the current weather and wind strength.
    """

    effect = WEATHER_EFFECTS[weather]
    return effect.solar_ratio, effect.wind_ratio(wind), effect.hydro_ratio
