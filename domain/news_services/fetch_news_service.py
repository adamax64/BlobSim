from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.news import News
from data.persistence.news_repository import get_all_news
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.news_dto import NewsDto, NewsTypeDto, TransfersDto
from domain.utils.sim_time_utils import convert_to_sim_time


@transactional
def fetch_all_news(session: Session) -> list[NewsDto]:
    all_news = get_all_news(session)

    result: list[NewsDto] = []
    for news in all_news:
        transfers = None
        retired = None
        rookies = None

        if news.news_type == NewsTypeDto.NEW_SEASON:
            (index, transfers) = _get_transfers(news.news_data)
            (index, retired) = _get_retired(index, news.news_data)
            rookies = _get_rookies(index, news.news_data)

        result.append(
            NewsDto(
                date=convert_to_sim_time(news.date),
                type=news.news_type,
                blob_name=_get_blob_name(news),
                league_name=_get_league_name(news),
                round=_get_round(news),
                season=_get_season(news),
                event_type=_get_event_type(news),
                winner=_get_winner(news),
                second=news.news_data[3] if news.news_type == NewsTypeDto.EVENT_ENDED else None,
                third=news.news_data[4] if news.news_type == NewsTypeDto.EVENT_ENDED else None,
                grandmaster=news.news_data[0] if news.news_type == NewsTypeDto.NEW_GRANDMASTER else None,
                transfers=transfers,
                retired=retired,
                rookies=rookies,
            )
        )
    return result


def _get_blob_name(news: News) -> str | None:
    return news.news_data[0] if news.news_type in [NewsTypeDto.BLOB_CREATED, NewsTypeDto.BLOB_TERMINATED] else None


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


def _get_winner(news: News) -> str | None:
    if news.news_type == NewsTypeDto.EVENT_ENDED:
        return news.news_data[2]
    if news.news_type == NewsTypeDto.SEASON_ENDED:
        return news.news_data[1]
    if news.news_type == NewsTypeDto.ROOKIE_OF_THE_YEAR:
        return news.news_data[0]
    return None


def _get_transfers(data: list[str]) -> tuple[int, list[TransfersDto]]:
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
            transfer.blobs.append(data[index])
        result.append(transfer)

    return result


def _get_retired(index: int, data: list[str]) -> tuple[int, list[str]]:
    result: list[str] = []

    index += 1
    retired_num = int(data[index])
    for _ in range(retired_num):
        index += 1
        result.append(data[index])

    return result


def _get_rookies(index: int, data: list[str]) -> list[str]:
    result: list[str] = []

    index += 1
    rookies_num = int(data[index])
    for _ in range(rookies_num):
        index += 1
        result.append(data[index])

    return result
