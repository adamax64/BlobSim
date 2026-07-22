from pydantic import BaseModel


class FactoryProgressDto(BaseModel):
    progress: float
    solar_efficiency: float
    wind_efficiency: float
    hydro_efficiency: float
