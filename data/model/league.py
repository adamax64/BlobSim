from sqlalchemy import Column, Integer, String, TypeDecorator
from sqlalchemy.orm import relationship

from data.db.db_engine import Base
from data.model.translation import Translation


class TranslationType(TypeDecorator):
    """Custom type for PostgreSQL translation composite type."""

    impl = String
    cache_ok = True

    def process_result_value(self, value, dialect):
        """Convert psycopg2 namedtuple to Translation object."""
        if value is not None:
            # psycopg2 returns namedtuple with .en, .hu attributes
            return Translation(en=getattr(value, "en", ""), hu=getattr(value, "hu", ""))
        return Translation(en="", hu="")

    def process_bind_param(self, value, dialect):
        """Convert Translation object to tuple for PostgreSQL composite type."""
        if value is not None:
            if isinstance(value, Translation):
                return (value.en, value.hu)
            elif isinstance(value, dict):
                return (value.get("en", ""), value.get("hu", ""))
        return ("", "")


class League(Base):
    __tablename__ = "leagues"
    __table_args__ = {"schema": "BCS"}

    id = Column(Integer, primary_key=True)
    name = Column(TranslationType, nullable=False)
    level = Column(Integer, unique=True)
    players = relationship("Blob", backref="leagues", overlaps="blobs,league")

    def __init__(self, *args, **kwargs):
        # Handle Translation object in name parameter
        if "name" in kwargs and isinstance(kwargs["name"], Translation):
            translation = kwargs.pop("name")
            kwargs["name"] = translation
        super().__init__(*args, **kwargs)

    def get_translation(self) -> Translation:
        """Return name as Translation object."""
        return self.name

    def set_translation(self, translation: Translation) -> None:
        """Set name from Translation object."""
        self.name = translation
