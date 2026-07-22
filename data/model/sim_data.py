from sqlalchemy import Column, Enum, Float, Integer, BigInteger

from data.db.db_engine import Base
from data.model.weather_type import WeatherType
from data.model.season_temperature import SeasonTemperature


class SimData(Base):
    __tablename__ = 'sim_data'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    sim_time = Column(BigInteger)
    factory_progress = Column(Integer)
    weather = Column(Enum(WeatherType))
    wind = Column(Float)
    season_temperature = Column(Enum(SeasonTemperature))
