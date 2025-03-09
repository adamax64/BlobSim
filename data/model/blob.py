from sqlalchemy import Column, ForeignKey, Integer, String, Double, BigInteger
from sqlalchemy.orm import relationship

from data.db.db_engine import Base


class Blob(Base):
    __tablename__ = 'blobs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    strength = Column(Double)
    learning = Column(Double)
    integrity = Column(Integer)
    born = Column(BigInteger)
    terminated = Column(BigInteger, default=None)
    debut = Column(Integer)
    contract = Column(Integer)
    money = Column(Integer, default=0)
    points = Column(Integer, default=0)
    bronze_medals = Column(Integer, default=0)
    silver_medals = Column(Integer, default=0)
    gold_medals = Column(Integer, default=0)
    season_victories = Column(Integer, default=0)
    bronze_trophies = Column(Integer, default=0)
    silver_trophies = Column(Integer, default=0)
    gold_trophies = Column(Integer, default=0)
    championships = Column(Integer, default=0)
    grandmasters = Column(Integer, default=0)
    league_id = Column(Integer, ForeignKey('leagues.id'))
    league = relationship('League', backref='blobs', overlaps='blobs,league', viewonly=True)
