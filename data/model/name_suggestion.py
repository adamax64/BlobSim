from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from data.db.db_engine import Base


class NameSuggestion(Base):
    __tablename__ = 'name_suggestions'
    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', name='unique_full_name'),
        {'schema': 'BCS'}
    )

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('BCS.blobs.id'), default=None)
    created = Column(DateTime)
