from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.news import News
from data.persistence.news_repository import get_all_news
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.news_dto import NewsDto, NewsTypeDto, TransfersDto
from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.utils.sim_time_utils import convert_to_sim_time
from domain.blob_services.blob_fetching_service import fetch_blob_by_id


@transactional
def fetch_all_news(session: Session) -> list[NewsDto]:
    all_news = get_all_news(session)

    result: list[NewsDto] = []
    for news in all_news:
        transfers = None
        retired = None
        rookies = None

        if news.news_type == NewsTypeDto.NEW_SEASON:
            (index, transfers) = _get_transfers(news.news_data, session)
            (index, retired) = _get_retired(index, news.news_data, session)
            rookies = _get_rookies(index, news.news_data, session)

        result.append(
            NewsDto(
                date=convert_to_sim_time(news.date),
                type=news.news_type,
                blob=_get_blob(news, session),
                league_name=_get_league_name(news),
                round=_get_round(news),
                season=_get_season(news),
                event_type=_get_event_type(news),
                winner=_get_winner(news, session),
                second=_get_second(news, session),
                third=_get_third(news, session),
                grandmaster=_get_grandmaster(news, session),
                transfers=transfers,
                retired=retired,
                rookies=rookies,
            )
        )
    return result


def _get_blob(news: News, session) -> BlobStatsDto | None:
    if news.news_type in [NewsTypeDto.BLOB_CREATED, NewsTypeDto.BLOB_TERMINATED]:
        try:
            return fetch_blob_by_id(int(news.news_data[0]), session)
        except Exception:
            return None
    return None


def _get_league_name(news: News) -> str | None:
    return (
        news.news_data[0]
        if news.news_type in [
            NewsTypeDto.EVENT_STARTED,
            NewsTypeDto.ONGOING_EVENT,
            NewsTypeDto.EVENT_ENDED,
            NewsTypeDto.SEASON_ENDED,
        ]
        else None
    )


def _get_round(news: News) -> int | None:
    return (
        int(news.news_data[1])
        if news.news_type in [
            NewsTypeDto.EVENT_STARTED,
            NewsTypeDto.ONGOING_EVENT,
            NewsTypeDto.EVENT_ENDED,
        ]
        else None
    )


def _get_season(news: News) -> int | None:
    return int(news.news_data[0]) if news.news_type == NewsTypeDto.NEW_SEASON else None


def _get_event_type(news: News) -> EventTypeDto | None:
    return news.news_data[2] if news.news_type in [NewsTypeDto.EVENT_STARTED, NewsTypeDto.ONGOING_EVENT] else None


def _get_winner(news: News, session) -> BlobStatsDto | None:
    try:
        if news.news_type == NewsTypeDto.EVENT_ENDED:
            return fetch_blob_by_id(int(news.news_data[2]), session)
        if news.news_type == NewsTypeDto.SEASON_ENDED:
            return fetch_blob_by_id(int(news.news_data[1]), session)
        if news.news_type == NewsTypeDto.ROOKIE_OF_THE_YEAR:
            return fetch_blob_by_id(int(news.news_data[0]), session)
    except Exception:
        return None
    return None


def _get_second(news: News, session) -> BlobStatsDto | None:
    try:
        return fetch_blob_by_id(int(news.news_data[3]), session) if news.news_type == NewsTypeDto.EVENT_ENDED else None
    except Exception:
        return None


def _get_third(news: News, session) -> BlobStatsDto | None:
    try:
        return fetch_blob_by_id(int(news.news_data[4]), session) if news.news_type == NewsTypeDto.EVENT_ENDED else None
    except Exception:
        return None


def _get_grandmaster(news: News, session) -> BlobStatsDto | None:
    try:
        return fetch_blob_by_id(int(news.news_data[0]), session) if news.news_type == NewsTypeDto.NEW_GRANDMASTER else None
    except Exception:
        return None


def _get_transfers(data: list[str], session) -> tuple[int, list[TransfersDto]]:
    result: list[TransfersDto] = []

    index = 1
    league_num = int(data[index])
    for _ in range(league_num):
        index += 1
        transfer = TransfersDto(data[index], [])
        index += 1
        blobs_num = int(data[index])
        for _ in range(blobs_num):
            index += 1
            try:
                transfer.blobs.append(fetch_blob_by_id(int(data[index]), session))
            except Exception:
                # skip if cannot map
                pass
        result.append(transfer)

    return (index, result)


def _get_retired(index: int, data: list[str], session) -> tuple[int, list[BlobStatsDto]]:
    result: list[BlobStatsDto] = []

    index += 1
    retired_num = int(data[index])
    for _ in range(retired_num):
        index += 1
        try:
            result.append(fetch_blob_by_id(int(data[index]), session))
        except Exception:
            pass

    return (index, result)


def _get_rookies(index: int, data: list[str], session) -> list[BlobStatsDto]:
    result: list[BlobStatsDto] = []

    index += 1
    rookies_num = int(data[index])
    for _ in range(rookies_num):
        index += 1
        try:
            result.append(fetch_blob_by_id(int(data[index]), session))
        except Exception:
            pass

    return result
