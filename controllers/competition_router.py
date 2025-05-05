from fastapi import APIRouter, HTTPException
from domain.competition_service import load_competition_data
from domain.dtos.event_dto import EventDto
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
