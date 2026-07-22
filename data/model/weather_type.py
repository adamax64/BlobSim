import enum


class WeatherType(enum.Enum):
    """
    Enum for Weather Type
    """

    SUNNY = "SUNNY"
    SUNNY_CLOUDY = "SUNNY_CLOUDY"
    CLOUDY = "CLOUDY"
    SUNNY_RAIN = "SUNNY_RAIN"
    RAIN = "RAIN"
    HEAVY_RAIN = "HEAVY_RAIN"
    STORM = "STORM"
    HEAT = "HEAT"
    SNOWY = "SNOWY"
    FREEZY = "FREEZY"
    FOGGY = "FOGGY"
