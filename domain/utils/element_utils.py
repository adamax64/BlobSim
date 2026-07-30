from typing import Dict, Tuple

from domain.enums.element_dto import ElementDto
from domain.enums.season_temperature import SeasonTemperatureDto
from domain.enums.weather_type import WeatherTypeDto


# Weather-dependent base buff/debuff percentage for FIRE, WATER, ICE and BEAST elements.
# The WIND element's buff instead depends on the day's wind strength (see `compute_wind_buff`),
# so it has no entry here.
ELEMENT_WEATHER_MODIFIERS: Dict[ElementDto, Dict[WeatherTypeDto, float]] = {
    ElementDto.FIRE: {
        WeatherTypeDto.SUNNY: 0.05,
        WeatherTypeDto.SUNNY_CLOUDY: 0.01,
        WeatherTypeDto.CLOUDY: 0.0,
        WeatherTypeDto.SUNNY_RAIN: 0.0,
        WeatherTypeDto.RAIN: -0.02,
        WeatherTypeDto.HEAVY_RAIN: -0.03,
        WeatherTypeDto.STORM: -0.04,
        WeatherTypeDto.HEAT: 0.10,
        WeatherTypeDto.SNOWY: -0.06,
        WeatherTypeDto.FREEZY: -0.10,
        WeatherTypeDto.FOGGY: 0.0,
    },
    ElementDto.WATER: {
        WeatherTypeDto.SUNNY: -0.05,
        WeatherTypeDto.SUNNY_CLOUDY: -0.01,
        WeatherTypeDto.CLOUDY: 0.0,
        WeatherTypeDto.SUNNY_RAIN: 0.02,
        WeatherTypeDto.RAIN: 0.05,
        WeatherTypeDto.HEAVY_RAIN: 0.10,
        WeatherTypeDto.STORM: 0.06,
        WeatherTypeDto.HEAT: -0.10,
        WeatherTypeDto.SNOWY: -0.05,
        WeatherTypeDto.FREEZY: -0.10,
        WeatherTypeDto.FOGGY: 0.0,
    },
    ElementDto.ICE: {
        WeatherTypeDto.SUNNY: -0.06,
        WeatherTypeDto.SUNNY_CLOUDY: -0.02,
        WeatherTypeDto.CLOUDY: 0.0,
        WeatherTypeDto.SUNNY_RAIN: 0.0,
        WeatherTypeDto.RAIN: 0.0,
        WeatherTypeDto.HEAVY_RAIN: 0.0,
        WeatherTypeDto.STORM: 0.0,
        WeatherTypeDto.HEAT: -0.12,
        WeatherTypeDto.SNOWY: 0.06,
        WeatherTypeDto.FREEZY: 0.12,
        WeatherTypeDto.FOGGY: 0.0,
    },
    ElementDto.BEAST: {
        WeatherTypeDto.SUNNY: 0.0,
        WeatherTypeDto.SUNNY_CLOUDY: 0.0,
        WeatherTypeDto.CLOUDY: 0.0,
        WeatherTypeDto.SUNNY_RAIN: -0.02,
        WeatherTypeDto.RAIN: -0.05,
        WeatherTypeDto.HEAVY_RAIN: -0.08,
        WeatherTypeDto.STORM: -0.10,
        WeatherTypeDto.HEAT: -0.03,
        WeatherTypeDto.SNOWY: 0.0,
        WeatherTypeDto.FREEZY: 0.0,
        WeatherTypeDto.FOGGY: 0.04,
    },
}

# Wind element's weather-independent buff/debuff range.
WIND_BUFF_MIN = -0.05
WIND_BUFF_MAX = 0.05

# Weather-dependent penalties applied to blobs that have no element at all.
NO_ELEMENT_WEATHER_SPEED_PENALTIES: Dict[WeatherTypeDto, float] = {
    WeatherTypeDto.RAIN: -0.01,
    WeatherTypeDto.HEAVY_RAIN: -0.02,
    WeatherTypeDto.HEAT: -0.02,
    WeatherTypeDto.FREEZY: -0.02,
}
NO_ELEMENT_WEATHER_STRENGTH_PENALTIES: Dict[WeatherTypeDto, float] = {
    WeatherTypeDto.HEAT: -0.02,
    WeatherTypeDto.FREEZY: -0.02,
}


def compute_wind_buff(wind: float) -> float:
    """Linearly map a wind value (0..1) to the Wind element's -5%..+5% buff range."""
    return (wind - 0.5) * (WIND_BUFF_MAX - WIND_BUFF_MIN)


def compute_element_skill_multipliers(
    element: ElementDto | None,
    weather: WeatherTypeDto | None,
    wind: float,
    season_temperature: SeasonTemperatureDto | None,
) -> Tuple[float, float]:
    """
    Compute (strength_multiplier, speed_multiplier) for a blob's element given the current
    weather/wind/season temperature. If the blob has no element, weather can still apply
    small penalties (rain/heavy rain/heat/freeze). Missing weather/season temperature are
    treated as neutral (no bonus/penalty from them).
    """
    if element is None or element == ElementDto.NONE:
        if weather is None:
            return 1.0, 1.0
        strength_bonus = NO_ELEMENT_WEATHER_STRENGTH_PENALTIES.get(weather, 0.0)
        speed_bonus = NO_ELEMENT_WEATHER_SPEED_PENALTIES.get(weather, 0.0)
        return 1.0 + strength_bonus, 1.0 + speed_bonus

    strength_bonus = 0.0
    speed_bonus = 0.0

    if element == ElementDto.WIND:
        wind_bonus = compute_wind_buff(wind)
        strength_bonus += wind_bonus
        speed_bonus += wind_bonus
    elif weather is not None:
        weather_bonus = ELEMENT_WEATHER_MODIFIERS.get(element, {}).get(weather, 0.0)
        strength_bonus += weather_bonus
        speed_bonus += weather_bonus

    if element == ElementDto.FIRE and season_temperature != SeasonTemperatureDto.COLD:
        strength_bonus += 0.02

    if element == ElementDto.WIND and weather is not None and weather != WeatherTypeDto.FOGGY:
        speed_bonus += 0.02

    if element == ElementDto.ICE:
        speed_bonus += 0.01
        if season_temperature == SeasonTemperatureDto.COLD:
            strength_bonus += 0.01
        else:
            strength_bonus -= 0.01

    if element == ElementDto.BEAST:
        strength_bonus += 0.02
        speed_bonus += 0.02

    return 1.0 + strength_bonus, 1.0 + speed_bonus
