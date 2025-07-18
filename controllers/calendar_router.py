from fastapi import APIRouter, HTTPException
import traceback
from domain.calendar_service import get_season_calendar as service_get_season_calendar
from domain.dtos.calendar_dto import CalendarDto


router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("")
def get_season_calendar() -> list[CalendarDto]:
    """
    Get the season calendar.
    """
    try:
        return service_get_season_calendar()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=e.with_traceback(None))
