from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from data.db.db_engine import Base


class League(Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(Integer, unique=True)
    players = relationship('Blob', backref='leagues', overlaps='blobs,league')
