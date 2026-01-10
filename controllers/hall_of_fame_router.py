import traceback
from fastapi import APIRouter, HTTPException

from domain.dtos.records_by_event_dto import RecordsByEventDto
from domain.dtos.titles_count_dto import TitlesCountSummaryDto
from domain.hall_of_fame_services.titles_chronology_service import get_titles_chronology as get_titles_chronology_service
from domain.hall_of_fame_services.titles_count_service import get_titles_count as get_titles_count_summary_service
from domain.hall_of_fame_services.records_by_event_service import get_records_by_event_type as get_records_by_event_type_service
from domain.dtos.titles_chronology_dto import TitlesChronologyDto

router = APIRouter()


@router.get("/hall-of-fame/chronology", response_model=TitlesChronologyDto)
async def get_titles_chronology() -> TitlesChronologyDto:
    """Fetch the chronology of titles awarded over the seasons."""
    try:
        return get_titles_chronology_service()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.get("/hall-of-fame/titles", response_model=TitlesCountSummaryDto)
async def get_titles_count_summary() -> TitlesCountSummaryDto:
    """Fetch the count of the following:
    - Grandmaster titles
    - Top league championships
    - Top league wins
    - Top league podiums
    - Lower league season victories
    - Lower league wins
    - Lower league podiums."""
    try:
        return get_titles_count_summary_service()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")


@router.get("/hall-of-fame/records-by-event", response_model=RecordsByEventDto)
async def get_records_by_event_type() -> RecordsByEventDto:
    """Fetch wins and records organized by event type and league."""
    try:
        return get_records_by_event_type_service()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
