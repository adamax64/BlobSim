from sqlalchemy import Column, Double, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base
from data.model.event_type import EventType


class Record(Base):
    __tablename__ = 'records'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey('BCS.leagues.id'))
    league = relationship('League', backref='records')
    event_type = Column(Enum(EventType))
    competitor_id = Column(Integer, ForeignKey('BCS.blobs.id'))
    competitor = relationship('Blob', backref='records')
    score = Column(Double)
