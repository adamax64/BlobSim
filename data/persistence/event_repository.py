from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.event import Event
from data.model.event_type import EventType


@transactional
def get_event_by_id(session: Session, event_id: int) -> Event | None:
    return session.query(Event).filter(Event.id == event_id).first()


@transactional
def get_event_by_date(session: Session, date: int) -> Event | None:
    return session.query(Event).filter(Event.date == date).first()


@transactional
def get_previous_event_by_league_id_and_season(session: Session, league_id: int, season: int) -> Event | None:
    return session.query(Event).filter(Event.league_id == league_id, Event.season == season).order_by(Event.date.desc()).first()


@transactional
def get_events_by_season(session: Session, season: int, exclude_non_competition: bool = False) -> list[Event]:
    """Return all events for the given season, ordered by date (sim time)."""
    query = session.query(Event).filter(Event.season == season).order_by(Event.date)
    if exclude_non_competition:
        query = query.filter(Event.type != EventType.CATCHUP_TRAINING)
    return query.all()


@transactional
def save_event(session: Session, event: Event) -> Event:
    session.add(event)
    session.commit()
    session.refresh(event)
    return event
