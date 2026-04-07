from sqlalchemy import Boolean, Column, Integer

from data.db.db_engine import Base


class AdminSettings(Base):
    __tablename__ = "admin_settings"
    __table_args__ = {"schema": "BCS"}

    id = Column(Integer, primary_key=True)
    enable_cronjobs = Column(Boolean, nullable=False, unique=True)
