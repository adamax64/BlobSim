import random
from typing import Dict

from domain.enums.weather_type import WeatherTypeDto
from domain.enums.season_temperature import SeasonTemperatureDto

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


def choose_weather(season_temperature: SeasonTemperatureDto) -> WeatherTypeDto:
    """Randomly pick a weather type, weighted by rarity for the given season temperature"""

    rarity = WEATHER_RARITY[season_temperature]
    weather_types = list(rarity.keys())
    weights = list(rarity.values())
    return random.choices(weather_types, weights=weights, k=1)[0]


def choose_wind() -> float:
    """Randomly pick a wind strength between 0 and 1"""

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
