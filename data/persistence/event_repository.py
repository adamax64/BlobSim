from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.event import Event


@transactional
def get_event_by_date(session: Session, date: int) -> Event | None:
    return session.query(Event).filter(Event.date == date).first()


@transactional
def get_previous_event_by_league_id_and_season(session: Session, league_id: int, season: int) -> Event | None:
    return session.query(Event).filter(Event.league_id == league_id, Event.season == season).order_by(Event.date.desc()).first()


@transactional
def save_event(session: Session, event: Event) -> Event:
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
