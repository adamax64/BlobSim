from typing import List
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.league import League


@transactional
def get_all_leagues_ordered_by_level(session: Session) -> List[League]:
    return session.query(League).order_by(League.level).all()


@transactional
def get_all_real_leagues(session: Session) -> List[League]:
    result = session.query(League).filter(League.name.notlike('queue')).all()
    return result


@transactional
def get_queue(session: Session) -> League:
    return session.query(League).filter(League.name.like('queue')).first()


@transactional
def get_league_by_id(session: Session, league_id: int) -> League | None:
    return session.query(League).filter(League.id == league_id).first()


@transactional
def save_league(session: Session, league: League) -> League:
    session.add(league)
    session.commit()
    session.refresh(league)
    return league
