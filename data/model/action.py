from sqlalchemy import Column, Double, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base


class Action(Base):
    __tablename__ = 'actions'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('BCS.events.id'))
    event = relationship('Event', back_populates='actions')  # Use back_populates
    tick = Column(Integer)
    blob_id = Column(Integer, ForeignKey('BCS.blobs.id'))
    blob = relationship('Blob', backref='actions')
    score = Column(Double)
