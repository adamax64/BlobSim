from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base


class Result(Base):
    __tablename__ = 'results'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('BCS.events.id'))
    event = relationship('Event', backref='results')
    blob_id = Column(Integer, ForeignKey('BCS.blobs.id'))
    blob = relationship('Blob', backref='results')
    position = Column(Integer)
    points = Column(Integer)
