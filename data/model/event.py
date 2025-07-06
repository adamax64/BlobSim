from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base
from .event_type import EventType


class Event(Base):
    __tablename__ = 'events'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey('BCS.leagues.id'))
    league = relationship('League', backref='events')
    actions = relationship('Action', back_populates='event')  # Use back_populates
    date = Column(BigInteger, default=None)
    season = Column(Integer)
    round = Column(Integer)
    type = Column(Enum(EventType))
