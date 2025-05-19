from pydantic import BaseModel
from enum import Enum
from fastapi import APIRouter, HTTPException

from domain.blob_service import check_blob_created
from domain.dtos.event_summary_dto import EventSummaryDTO
from domain.event_service import get_concluded_event_summary
from domain.sim_data_service import get_sim_time, is_unconcluded_event_today
from domain.utils.sim_time_utils import is_season_start


class NewsType(str, Enum):
    EVENT = "EVENT"
    EVENT_ENDED = "EVENT_ENDED"
    BLOB_CREATED_AND_NAMED = "BLOB_CREATED_AND_NAMED"
    BLOB_CREATED = "BLOB_CREATED"
    SEASON_START = "SEASON_START"
    CONTINUE = "CONTINUE"


class News(BaseModel):
    news_type: NewsType
    blob_info: str = None
    event_summary: EventSummaryDTO = None


router = APIRouter(prefix="/general-infos", tags=["general-infos"])


@router.get("/news")
def get_news() -> list[News]:
    try:
        options = []

        if is_unconcluded_event_today():
            options.append(News(news_type=NewsType.EVENT))

        event_summary = get_concluded_event_summary()
        if event_summary is not None:
            options.append(
                News(
                    news_type=NewsType.EVENT_ENDED,
                    event_summary=event_summary,
                )
            )

        created_blob_check = check_blob_created()
        if isinstance(created_blob_check, str):
            options.append(
                News(
                    news_type=NewsType.BLOB_CREATED_AND_NAMED,
                    blob_info=created_blob_check,
                )
            )
        elif created_blob_check:
            options.append(News(news_type=NewsType.BLOB_CREATED))

        if is_season_start(get_sim_time()):
            options.append(News(news_type=NewsType.SEASON_START))

        if len(options) == 0:
            options.append(News(news_type=NewsType.CONTINUE))

        return options
    except Exception as e:
        print(str(e.with_traceback(None)))
        raise HTTPException(status_code=500, detail=f"{e.with_traceback(None)}")
