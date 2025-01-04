from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base
from .event_type import EventType


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey('leagues.id'))
    league = relationship('League', backref='events')
    actions = relationship('Action', backref='event')
    date = Column(BigInteger, default=None)
    season = Column(Integer)
    round = Column(Integer)
    type = Column(Enum(EventType))
