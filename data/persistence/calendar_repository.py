from typing import Dict, List
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.calendar import Calendar
from data.model.event import Event


@transactional
def get_calendar(session: Session) -> Dict[int, Calendar]:
    result = session.query(Calendar).order_by(Calendar.date).all()
    return {record.date: record for record in result}


@transactional
def count_unconcluded_for_league(session: Session, league_id: int) -> int:
    return session.query(Calendar).filter(Calendar.league_id == league_id, Calendar.concluded.is_(False)).count()


@transactional
def get_next_unconcluded(session: Session) -> Calendar:
    return session.query(Calendar).filter(Calendar.concluded.is_(False)).order_by(Calendar.date).first()


@transactional
def save_calendar_event(session: Session, event: Event):
    session.add(event)


@transactional
def save_all_calendar_records(session: Session, records: List[Calendar]):
    session.add_all(records)
    session.commit()


@transactional
def clear_calendar(session: Session):
    session.query(Calendar).delete()
    session.commit()
