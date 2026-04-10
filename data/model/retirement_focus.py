from sqlalchemy import Column, Enum, ForeignKey, Integer

from data.db.db_engine import Base
from data.model.retirement_focus_type import RetirementFocusType


class RetirementFocus(Base):
    __tablename__ = "retirement_focus"
    __table_args__ = {"schema": "BCS"}

    id = Column(Integer, primary_key=True)
    blob_id = Column(Integer, ForeignKey("BCS.blobs.id"), unique=True, nullable=False)
    focus_type = Column(Enum(RetirementFocusType), nullable=False)
