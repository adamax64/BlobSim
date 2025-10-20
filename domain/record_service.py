from data.persistence.record_repository import (
    get_record_by_league_and_event_type,
    get_all_records_by_league,
    get_all_records_by_event_type,
    get_all_records,
    is_score_new_record,
    update_record_if_better
)
from data.model.event_type import EventType
from domain.dtos.record_dto import RecordDto
from data.db.db_engine import transactional


@transactional
def get_record_for_league_and_event_type(league_id: int, event_type: EventType, session) -> RecordDto | None:
    """Get the current record for a specific league and event type."""
    record = get_record_by_league_and_event_type(session, league_id, event_type)
    if record:
        return RecordDto(
            id=record.id,
            league_id=record.league_id,
            event_type=record.event_type,
            competitor_id=record.competitor_id,
            score=record.score
        )
    return None


@transactional
def get_records_for_league(league_id: int, session) -> list[RecordDto]:
    """Get all records for a specific league."""
    records = get_all_records_by_league(session, league_id)
    return [
        RecordDto(
            id=record.id,
            league_id=record.league_id,
            event_type=record.event_type,
            competitor_id=record.competitor_id,
            score=record.score
        )
        for record in records
    ]


@transactional
def get_records_for_event_type(event_type: EventType, session) -> list[RecordDto]:
    """Get all records for a specific event type."""
    records = get_all_records_by_event_type(session, event_type)
    return [
        RecordDto(
            id=record.id,
            league_id=record.league_id,
            event_type=record.event_type,
            competitor_id=record.competitor_id,
            score=record.score
        )
        for record in records
    ]


@transactional
def get_all_records_service(session) -> list[RecordDto]:
    """Get all records in the system."""
    records = get_all_records(session)
    return [
        RecordDto(
            id=record.id,
            league_id=record.league_id,
            event_type=record.event_type,
            competitor_id=record.competitor_id,
            score=record.score
        )
        for record in records
    ]


@transactional
def check_and_update_record(league_id: int, event_type: EventType, competitor_id: int, score: float, session) -> bool:
    """
    Check if a score is a new record and update if it is.
    Returns True if a new record was set, False otherwise.
    """
    return update_record_if_better(session, league_id, event_type, competitor_id, score)


@transactional
def is_new_record(league_id: int, event_type: EventType, score: float, session) -> bool:
    """Check if a score would be a new record without updating."""
    return is_score_new_record(session, league_id, event_type, score)
