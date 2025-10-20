from fastapi import APIRouter, Depends

from domain.record_service import (
    get_record_for_league_and_event_type,
    get_records_for_league,
    get_records_for_event_type,
    get_all_records_service
)
from domain.dtos.record_dto import RecordDto
from data.model.event_type import EventType
from controllers.auth_dependency import require_auth

router = APIRouter()


# TODO: These routes are not used anywhere yet, but should be kept for future features.
# TODO: Consider removing them when that new feature is implemented and they are not used.

@router.get("/records/league/{league_id}")
async def get_league_records(league_id: int, _=Depends(require_auth)) -> list[RecordDto]:
    """Get all records for a specific league."""
    return get_records_for_league(league_id)


@router.get("/records/event-type/{event_type}")
async def get_event_type_records(
    event_type: EventType,
    _=Depends(require_auth)
) -> list[RecordDto]:
    """Get all records for a specific event type."""
    return get_records_for_event_type(event_type)


@router.get("/records/league/{league_id}/event-type/{event_type}")
async def get_league_event_type_record(
    league_id: int,
    event_type: EventType,
    _=Depends(require_auth)
) -> RecordDto | None:
    """Get the current record for a specific league and event type combination."""
    return get_record_for_league_and_event_type(league_id, event_type)


@router.get("/records")
async def get_all_records(_=Depends(require_auth)) -> list[RecordDto]:
    """Get all records in the system."""
    return get_all_records_service()
