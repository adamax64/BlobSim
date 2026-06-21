import enum


class StateType(enum.Enum):
    """
    Enum for State Type
    """

    INJURED = "INJURED"
    TIRED = "TIRED"
    GLOOMY = "GLOOMY"
    FOCUSED = "FOCUSED"

    # Boosted states caused by items
    COOKIE_BOOST = "COOKIE_BOOST"
    ENERGY_CELL_BOOST = "ENERGY_CELL_BOOST"
    CACHE_BOOST = "CACHE_BOOST"
    POWER_BANK_BOOST = "POWER_BANK_BOOST"
    OVERCLOCKING_DEVICE_BOOST = "OVERCLOCKING_DEVICE_BOOST"
