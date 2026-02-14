from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base
from data.model.trait_type import TraitType


class Trait(Base):
    __tablename__ = "traits"
    __table_args__ = {"schema": "BCS"}

    id = Column(Integer, primary_key=True)
    blob_id = Column(Integer, ForeignKey("BCS.blobs.id"), nullable=False)
    blob = relationship("Blob", backref="traits", viewonly=True)
    type = Column(Enum(TraitType), nullable=False)
