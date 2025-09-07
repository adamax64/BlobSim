from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Double, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship

from data.db.db_engine import Base
from data.model.activity_type import ActivityTypeDbo


class Blob(Base):
    __tablename__ = 'blobs'
    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', name='unique_blob_full_name'),
        {'schema': 'BCS'}
    )

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    strength = Column(Double)
    speed = Column(Double)
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
    league_id = Column(Integer, ForeignKey('BCS.leagues.id'))
    league = relationship('League', backref='blobs', overlaps='blobs,league', viewonly=True)
    parent_id = Column(Integer, ForeignKey('BCS.blobs.id'))
    parent = relationship('Blob', remote_side=[id], backref='children')
    color = Column(String, nullable=False, default="#888888")
    current_activity = Column(Enum(ActivityTypeDbo), default=ActivityTypeDbo.IDLE)
