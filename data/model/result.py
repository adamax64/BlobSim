from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', backref='results')
    blob_id = Column(Integer, ForeignKey('blobs.id'))
    blob = relationship('Blob', backref='results')
    position = Column(Integer)
    points = Column(Integer)
