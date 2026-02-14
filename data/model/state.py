from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from data.db.db_engine import Base
from data.model.state_type import StateType


class State(Base):
    __tablename__ = "states"
    __table_args__ = {"schema": "BCS"}

    id = Column(Integer, primary_key=True)
    blob_id = Column(Integer, ForeignKey("BCS.blobs.id"), nullable=False)
    blob = relationship("Blob", backref="states", viewonly=True)
    type = Column(Enum(StateType), nullable=False)
    effect_until = Column(BigInteger, nullable=False)
