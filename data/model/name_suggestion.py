from sqlalchemy import Column, DateTime, Integer, String
from data.db.db_engine import Base


class NameSuggestion(Base):
    __tablename__ = 'name_suggestions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    created = Column(DateTime)
