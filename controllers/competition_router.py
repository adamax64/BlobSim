from fastapi import APIRouter, HTTPException, Depends
import traceback
from domain.championship_service import end_eon_if_over, end_season_if_over
from domain.competition_service import (
    load_competition_data,
    process_event_results as service_save_event_results,
)
from domain.dtos.event_dto import EventDto
from domain.dtos.event_record_dto import EliminationEventRecordDto, EventRecordDto, QuarteredEventRecordDto, RaceEventRecordDto, SprintEventRecordDto
from domain.dtos.result_dto import ResultDto
from domain.exceptions.no_current_event_exception import NoCurrentEventException
from domain.result_service import get_results_for_event
from domain.sim_data_service import is_current_event_concluded
from .auth_dependency import require_auth


router = APIRouter(prefix="/competition", tags=["competition"])


@router.get("/current")
async def get_current_event() -> EventDto:
    try:
        event_data = load_competition_data()
        return event_data
    except NoCurrentEventException:
        raise HTTPException(status_code=400, detail="NO_CURRENT_EVENT")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.get("/results/event/{event_id}")
async def get_results_for_event_route(event_id: int) -> list[ResultDto]:
    """Get results for a specific event by id."""
    return get_results_for_event(event_id)


@router.post("/quartered-event-results")
async def save_quartered(event: EventDto, event_records: list[QuarteredEventRecordDto], _=Depends(require_auth)) -> None:
    """
    Save event results for quartered events.
    """
    _save_event_results(event, event_records)


@router.post("/endurance-event-results")
async def save_endurance(event: EventDto, event_records: list[RaceEventRecordDto], _=Depends(require_auth)) -> None:
    """
    Save event results for endurance events.
    """
    _save_event_results(event, event_records)


@router.post("/sprint-event-results")
async def save_sprint(event: EventDto, event_records: list[SprintEventRecordDto], _=Depends(require_auth)) -> None:
    """
    Save event results for sprint events.
    """
    _save_event_results(event, event_records)


@router.post("/elimination-event-results")
async def save_elimination(event: EventDto, event_records: list[EliminationEventRecordDto], _=Depends(require_auth)) -> None:
    """
    Save event results for elimination events.
    """
    _save_event_results(event, event_records)


def _save_event_results(event: EventDto, event_records: list[EventRecordDto]) -> None:
    if event_records is None or len(event_records) == 0:
        raise HTTPException(status_code=400, detail="EVENT_RECORDS_EMPTY")

    if is_current_event_concluded():
        raise HTTPException(status_code=400, detail="EVENT_ALREADY_CONCLUDED")

    try:
        service_save_event_results(event, event_records)
        end_season_if_over(event.league, event.season)
        end_eon_if_over(event.season, event.league)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
