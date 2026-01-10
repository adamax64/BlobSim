from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base


class Champion(Base):
    __tablename__ = 'champions'
    __table_args__ = {'schema': 'BCS'}

    league_id = Column(Integer, ForeignKey('BCS.leagues.id'), primary_key=True)
    league = relationship('League', backref='champions', viewonly=True)
    season = Column(Integer, primary_key=True)
    blob_id = Column(Integer, ForeignKey('BCS.blobs.id'), primary_key=True)
    blob = relationship('Blob', backref='champions', viewonly=True)
