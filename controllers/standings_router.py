from fastapi import APIRouter, HTTPException
import traceback

from domain.dtos.grandmaster_standings_dto import GrandmasterStandingsDTO
from domain.dtos.standings_dto import StandingsDTO
from domain.sim_data_service import get_sim_time
from domain.standings_service import get_grandmaster_standings, get_standings
from domain.utils.sim_time_utils import get_season


router = APIRouter(prefix="/standings", tags=["Standings"])


@router.get("/championship/{league_id}/{season}")
def get_standings_by_league_and_season(league_id: int, season: int) -> list[StandingsDTO]:
    """
    Fetch standings by league id and season.
    """
    try:
        current_season = current_season = get_season(get_sim_time())
        return get_standings(league_id, season, current_season)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.get("/grandmaster/{start_season}")
def get_grandmaster_standings_by_eon(start_season: int) -> list[GrandmasterStandingsDTO]:
    """
    Fetch grandmaster standings by starting season of eon.
    """
    try:
        current_season = get_season(get_sim_time())
        return get_grandmaster_standings(start_season, current_season)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
