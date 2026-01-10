from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base


class Grandmaster(Base):
    __tablename__ = 'grandmasters'
    __table_args__ = {'schema': 'BCS'}

    eon = Column(Integer, primary_key=True)
    blob_id = Column(Integer, ForeignKey('BCS.blobs.id'), primary_key=True)
    blob = relationship('Blob', backref='grandmaster_titles', viewonly=True)
