from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import CompositeType

from data.db.db_engine import Base
from data.model.translation import Translation


class _TranslationCompositeType(CompositeType):
    """Maps the "BCS".translation Postgres composite type to/from the Translation dataclass."""

    def bind_processor(self, dialect):
        parent = super().bind_processor(dialect)

        def process(value):
            if isinstance(value, Translation):
                value = {'en': value.en, 'hu': value.hu}
            return parent(value)

        return process

    def result_processor(self, dialect, coltype):
        parent = super().result_processor(dialect, coltype)

        def process(value):
            result = parent(value)
            return None if result is None else Translation(en=result.en, hu=result.hu)

        return process


# Kept unqualified: sqlalchemy_utils builds a namedtuple from this name, which must be a valid
# Python identifier. The schema needed to register this type with psycopg2 (since it doesn't
# live in 'public') is tracked separately, see TRANSLATION_TYPE_QUALIFIED_NAME below.
TRANSLATION_TYPE = _TranslationCompositeType(
    'translation',
    [
        Column('en', String),
        Column('hu', String),
    ],
)
TRANSLATION_TYPE_QUALIFIED_NAME = 'BCS.translation'


class League(Base):
    __tablename__ = 'leagues'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    name = Column(TRANSLATION_TYPE, nullable=False)
    level = Column(Integer, unique=True)
    players = relationship('Blob', backref='leagues', overlaps='blobs,league')
