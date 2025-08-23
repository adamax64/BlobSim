from fastapi import APIRouter, HTTPException, Depends
import traceback

from domain.action_service import create_actions_for_race, create_action_for_quartered_event
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.event_service import get_event_by_id
from domain.exceptions.event_not_found_exception import EventNotFoundException
from domain.exceptions.no_current_event_exception import NoCurrentEventException
from .auth_dependency import require_auth


router = APIRouter(prefix="/actions", tags=["actions"])


@router.post("/create/quartered")
def quartered(contender: BlobCompetitorDto, event_id: int, _=Depends(require_auth)):
    """
    Generate score for contender and save the action for given event.
    Returns: {"newRecord": bool}
    """
    try:
        new_record = create_action_for_quartered_event(contender, event_id)
        return {"newRecord": new_record}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.post("/create/race")
def race(event_id: int, tick: int, _=Depends(require_auth)):
    """
    Generate score for all contenders and save the actions for given event.
    """
    try:
        event = get_event_by_id(event_id, check_date=True)
    except NoCurrentEventException:
        raise HTTPException(status_code=400, detail="EVENT_IS_CONCLUDED")
    except EventNotFoundException:
        raise HTTPException(status_code=404, detail="EVENT_NOT_FOUND")

    try:
        create_actions_for_race(event.competitors, event_id, tick)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
