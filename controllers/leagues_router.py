from fastapi import APIRouter, HTTPException
import traceback
from domain.dtos.league_dto import LeagueDto
from domain.league_service import get_all_real_leagues

router = APIRouter(prefix="/leagues", tags=["Leagues"])


@router.get("/all", tags=["Leagues"])
def get_leagues() -> list[LeagueDto]:
    """
    Fetch all leagues excluding the queue.
    """
    try:
        return get_all_real_leagues()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
