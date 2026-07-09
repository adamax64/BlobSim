from sqlalchemy import Column, Enum, ForeignKey, Integer
from data.db.db_engine import Base
from data.model.item_type import ItemType


class Item(Base):
    __tablename__ = "items"
    __table_args__ = {"schema": "BCS"}

    id = Column(Integer, primary_key=True)
    type = Column(Enum(ItemType), nullable=False)
    blob_id = Column(Integer, ForeignKey("BCS.blobs.id"), nullable=False)
    durability = Column(Integer, nullable=False)
