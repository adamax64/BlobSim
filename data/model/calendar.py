from sqlalchemy import Column, BigInteger, Enum, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

from data.db.db_engine import Base
from data.model.event_type import EventType


class Calendar(Base):
    __tablename__ = 'calendar'

    date = Column(BigInteger, primary_key=True)
    league_id = Column(Integer, ForeignKey('leagues.id'))
    league = relationship('League', backref='calendar')
    concluded = Column(Boolean)
    event_type = Column(Enum(EventType))
