from sqlalchemy import ARRAY, BigInteger, Column, Enum, Integer, String
from data.db.db_engine import Base
from data.model.news_type import NewsTypeDbo


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    date = Column(BigInteger, nullable=False)
    news_type = Column(Enum(NewsTypeDbo), nullable=False)
    news_data = Column(ARRAY(String))
