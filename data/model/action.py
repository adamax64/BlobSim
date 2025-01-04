from sqlalchemy import Column, Double, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base


class Action(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    # event = relationship('Event', backref='action')
    tick = Column(Integer)
    blob_id = Column(Integer, ForeignKey('blobs.id'))
    blob = relationship('Blob', backref='actions')
    score = Column(Double)
