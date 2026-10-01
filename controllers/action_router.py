from fastapi import APIRouter, HTTPException, Depends
import traceback

from domain.action_service import (
    create_actions_for_elimination_event,
    create_actions_for_race,
    create_action_for_quartered_event,
)
from domain.dtos.blob_dtos.blob_competitor_dto import BlobCompetitorDto
from domain.event_record_services.event_record_service import get_event_records
from domain.event_record_services.quartered_event_record_service import (
    QuarteredEventRecordDto,
)
from domain.event_record_services.event_type_checks import is_quartered_event
from domain.event_service import get_event_by_id
from domain.exceptions.event_not_found_exception import EventNotFoundException
from domain.exceptions.no_current_event_exception import NoCurrentEventException
from .auth_dependency import require_auth

router = APIRouter(prefix="/actions", tags=["actions"])


@router.post("/create/quartered")
def quartered(event_id: int, _=Depends(require_auth)):
    """
    Generate score for the next contender and save the action for given event.
    Returns: {"name": str, "score": float} if new record, None otherwise
    """
    try:
        event = get_event_by_id(event_id, check_date=True)
    except NoCurrentEventException:
        raise HTTPException(status_code=400, detail="EVENT_IS_CONCLUDED")
    except EventNotFoundException:
        raise HTTPException(status_code=404, detail="EVENT_NOT_FOUND")

    if not is_quartered_event(event.type):
        raise HTTPException(status_code=400, detail="NOT_A_QUARTERED_EVENT")

    # Determine the next blob to act (same logic as progress_competition cronjob)
    event_records = get_event_records(event.actions, event.competitors, event.type)
    next_blob = next(
        (
            record.blob
            for record in event_records
            if isinstance(record, QuarteredEventRecordDto) and record.next
        ),
        None,
    )

    if next_blob is None:
        raise HTTPException(status_code=400, detail="NO_ACTIVE_COMPETITORS")

    try:
        record = create_action_for_quartered_event(next_blob, event_id)
        if record is not None:
            return {"name": record[0], "score": record[1]}
        return None
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/create/race")
def race(event_id: int, tick: int, _=Depends(require_auth)):
    """
    Generate score for all contenders and save the actions for given event.
    Returns: {"name": str, "score": float} if new record, None otherwise
    """
    try:
        event = get_event_by_id(event_id, check_date=True)
    except NoCurrentEventException:
        raise HTTPException(status_code=400, detail="EVENT_IS_CONCLUDED")
    except EventNotFoundException:
        raise HTTPException(status_code=404, detail="EVENT_NOT_FOUND")

    try:
        record = create_actions_for_race(event.competitors, event_id, tick)
        if record is not None:
            return {"name": record[0], "score": record[1]}
        return None
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/create/elimination")
def elimination(
    contenders: list[BlobCompetitorDto], event_id: int, _=Depends(require_auth)
):
    """
    Generate score for all contenders and save the actions for given event.
    """
    try:
        _ = get_event_by_id(event_id, check_date=True)
    except NoCurrentEventException:
        raise HTTPException(status_code=400, detail="EVENT_IS_CONCLUDED")
    except EventNotFoundException:
        raise HTTPException(status_code=404, detail="EVENT_NOT_FOUND")

    try:
        record = create_actions_for_elimination_event(contenders, event_id)
        if record is not None:
            return {"name": record[0], "score": record[1]}
        return None
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
