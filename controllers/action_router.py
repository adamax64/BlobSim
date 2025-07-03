from fastapi import APIRouter, HTTPException, Depends
import traceback

from domain.action_service import generate_and_save_all_actions, generate_score_and_save_action
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.event_service import get_event_by_id
from domain.exceptions.event_not_found_exception import EventNotFoundException
from domain.exceptions.no_current_event_exception import NoCurrentEventException
from .auth_dependency import require_auth


router = APIRouter(prefix="/actions", tags=["actions"])


@router.post("/create/quartered")
def quartered(contender: BlobCompetitorDto, event_id: int, tick: int, _=Depends(require_auth)):
    """
    Generate score for contender and save the action for given event.
    """
    try:
        generate_score_and_save_action(contender, event_id, tick)
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
        generate_and_save_all_actions(event.competitors, event_id, tick)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
