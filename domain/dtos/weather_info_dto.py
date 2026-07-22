from pydantic import BaseModel

from domain.enums.season_temperature import SeasonTemperatureDto
from domain.enums.weather_type import WeatherTypeDto


class WeatherInfoDto(BaseModel):
    weather: WeatherTypeDto
    wind: float
    season_temperature: SeasonTemperatureDto
