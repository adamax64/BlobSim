from pydantic import BaseModel
from enum import Enum
from fastapi import APIRouter

from domain.blob_service import check_blob_created
from domain.sim_data_service import get_sim_time, is_unconcluded_event_today
from domain.utils.sim_time_utils import is_season_start


class NewsType(str, Enum):
    EVENT = "EVENT"
    BLOB_CREATED_AND_NAMED = "BLOB_CREATED_AND_NAMED"
    BLOB_CREATED = "BLOB_CREATED"
    SEASON_START = "SEASON_START"
    CONTINUE = "CONTINUE"


class News(BaseModel):
    news_type: NewsType
    additional_info: str = None


router = APIRouter(prefix="/general-infos", tags=["general-infos"])


@router.get("/news")
def get_news() -> list[News]:
    try:
        options = []

        if is_unconcluded_event_today():
            options.append(News(news_type=NewsType.EVENT))

        created_blob_check = check_blob_created()
        if isinstance(created_blob_check, str):
            options.append(
                News(
                    news_type=NewsType.BLOB_CREATED_AND_NAMED,
                    additional_info=created_blob_check,
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
