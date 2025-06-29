from sqlalchemy import Column, Integer, BigInteger

from data.db.db_engine import Base


class SimData(Base):
    __tablename__ = 'sim_data'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    sim_time = Column(BigInteger)
    factory_progress = Column(Integer)
