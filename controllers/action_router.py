from fastapi import APIRouter, HTTPException

from domain.action_service import generate_score_and_save_action
from domain.dtos.blob_competitor_dto import BlobCompetitorDto


router = APIRouter(prefix="/actions", tags=["actions"])


@router.post("/create")
def create_action(contender: BlobCompetitorDto, event_id: int, tick: int) -> float:
    """
    Generate score for contender and save the action for given event.
    """
    try:
        return generate_score_and_save_action(contender, event_id, tick)
    except Exception as e:
        print(e.with_traceback(None))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
