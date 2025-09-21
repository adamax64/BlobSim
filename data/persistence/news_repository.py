from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.news import News
from data.model.news_type import NewsType
from data.persistence.sim_data_repository import get_sim_data


@transactional
def get_all_news(session: Session) -> list[News]:
    result: list[News] = session.query(News).order_by(News.date.desc()).all()
    return result


@transactional
def save_news(news: News, session: Session):
    session.add(news)
    session.commit()


@transactional
def delete_news_with_type(type: NewsType, session: Session):
    session.query(News).filter(News.news_type == type).delete(synchronize_session=False)
    session.commit()


@transactional
def delete_old_news(session: Session):
    days_threshold = 128
    threshold_date = get_sim_data(session).sim_time - days_threshold
    session.query(News).filter(News.date < threshold_date).delete(synchronize_session=False)
    session.commit()
