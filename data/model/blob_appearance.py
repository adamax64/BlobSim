from sqlalchemy import Column, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from data.db.db_engine import Base
from data.model.appearance_type import AppearanceType


class BlobAppearance(Base):
    __tablename__ = "blob_appearances"
    __table_args__ = (
        UniqueConstraint("blob_id", name="unique_blob_appearances_blob_id"),
        {"schema": "BCS"},
    )

    id = Column(Integer, primary_key=True)
    blob_id = Column(Integer, ForeignKey("BCS.blobs.id"), nullable=False)
    appearance_type = Column(
        Enum(AppearanceType), nullable=False, default=AppearanceType.SOLID
    )
    colors = Column(ARRAY(String), nullable=False)
    params = Column(ARRAY(String), nullable=False)

    blob = relationship("Blob", overlaps="blob,appearance", viewonly=True)
