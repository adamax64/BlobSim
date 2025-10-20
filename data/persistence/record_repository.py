from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.record import Record
from data.model.event_type import EventType


@transactional
def save_record(session: Session, record: Record) -> Record:
    session.add(record)
    session.commit()
    return record


@transactional
def get_record_by_league_and_event_type(session: Session, league_id: int, event_type: EventType) -> Record | None:
    return session.query(Record).filter(
        Record.league_id == league_id,
        Record.event_type == event_type
    ).first()


@transactional
def get_all_records_by_league(session: Session, league_id: int) -> list[Record]:
    return session.query(Record).filter(Record.league_id == league_id).all()


@transactional
def get_all_records_by_event_type(session: Session, event_type: EventType) -> list[Record]:
    return session.query(Record).filter(Record.event_type == event_type).all()


@transactional
def get_all_records(session: Session) -> list[Record]:
    return session.query(Record).all()


@transactional
def is_score_new_record(session: Session, league_id: int, event_type: EventType, score: float) -> bool:
    """
    Returns True if the given score is greater than the current record for the league and event type.
    """
    current_record = get_record_by_league_and_event_type(session, league_id, event_type)
    return (current_record is None) or (score > current_record.score)


@transactional
def update_record_if_better(session: Session, league_id: int, event_type: EventType, competitor_id: int, score: float) -> bool:
    """
    Updates the record if the new score is better than the current record.
    Returns True if a new record was set, False otherwise.
    """
    current_record = get_record_by_league_and_event_type(session, league_id, event_type)

    if current_record is None or score > current_record.score:
        if current_record is None:
            # Create new record
            new_record = Record(
                league_id=league_id,
                event_type=event_type,
                competitor_id=competitor_id,
                score=score
            )
            save_record(session, new_record)
        else:
            # Update existing record
            current_record.competitor_id = competitor_id
            current_record.score = score
            save_record(session, current_record)
        return True

    return False
