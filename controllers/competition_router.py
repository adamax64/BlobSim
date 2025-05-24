from fastapi import APIRouter, HTTPException
from domain.championship_service import end_eon_if_over, end_season_if_over
from domain.competition_service import (
    load_competition_data,
    save_event_results as service_save_event_results,
)
from domain.dtos.event_dto import EventDto
from domain.dtos.event_record_dto import EventRecordDto, QuarteredEventRecordDto, RaceEventRecordDto
from domain.exceptions.no_current_event_exception import NoCurrentEventException

router = APIRouter(prefix="/competition", tags=["competition"])


@router.get("/current")
async def get_current_event() -> EventDto:
    try:
        event_data = load_competition_data()
        return event_data
    except NoCurrentEventException:
        raise HTTPException(status_code=400, detail="NO_CURRENT_EVENT")
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/quartered-event-results")
async def save_quartered(event: EventDto, event_records: list[QuarteredEventRecordDto]) -> None:
    """
    Save event results for quartered events.
    """
    _save_event_results(event, event_records)


@router.post("/race-event-results")
async def save_race(event: EventDto, event_records: list[RaceEventRecordDto]) -> None:
    """
    Save event results for race events.
    """
    _save_event_results(event, event_records)


def _save_event_results(event: EventDto, event_records: list[EventRecordDto]):
    if event_records is None or len(event_records) == 0:
        raise HTTPException(status_code=400, detail="EVENT_RECORDS_EMPTY")

    try:
        service_save_event_results(event, event_records)
        end_season_if_over(event.league, event.season)
        end_eon_if_over(event.season, event.league)
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
