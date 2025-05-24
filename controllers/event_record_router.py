from fastapi import APIRouter, HTTPException

from domain.dtos.event_record_dto import EventRecordDto, QuarteredEventRecordDto, RaceEventRecordDto
from domain.event_record_service import get_event_records
from domain.event_service import get_event_by_id


router = APIRouter(prefix="/event-records", tags=["event-records"])


@router.get("/quartered", response_model=list[QuarteredEventRecordDto])
def get_quartered(event_id: int) -> list[QuarteredEventRecordDto]:
    """ Get quartered event records by actions. """
    return _get_event_records(event_id)


@router.get("/race", response_model=list[RaceEventRecordDto])
def get_race(event_id: int) -> list[RaceEventRecordDto]:
    """ Get race event records by actions. """
    return _get_event_records(event_id)


def _get_event_records(event_id: int) -> list[EventRecordDto]:
    event = None
    try:
        event = get_event_by_id(event_id)
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"Error querying event: {e.with_traceback(None)}")

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    try:
        return get_event_records(event.actions, event.competitors, event.type)
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"Error getting event records: {e.with_traceback(None)}")
