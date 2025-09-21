from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.event_type import EventType
from data.model.news import News
from data.model.news_type import NewsType
from data.persistence.news_repository import delete_news_with_type, delete_old_news, save_news
from domain.sim_data_service import get_sim_time


@transactional
def add_blob_created_news(blob_name: str, session: Session):
    _create_news(NewsType.BLOB_CREATED, [blob_name], session)
    delete_news_with_type(NewsType.BLOB_IN_CREATION, session)


@transactional
def add_blob_in_creation_news(session: Session):
    _create_news(NewsType.BLOB_IN_CREATION, [], session)


@transactional
def add_blob_terminated_news(blob_name: str, session: Session):
    _create_news(NewsType.BLOB_TERMINATED, [blob_name], session)


@transactional
def add_event_starting_news(league_name: str, round: int, event_type: EventType, session: Session):
    _create_news(NewsType.EVENT_STARTED, [league_name, str(round), event_type.name], session)


@transactional
def add_ongoing_event_news(league_name: str, round: int, event_type: EventType, session: Session):
    _create_news(NewsType.ONGOING_EVENT, [league_name, str(round), event_type.name], session)
    delete_news_with_type(NewsType.EVENT_STARTED, session)


@transactional
def add_event_ended_news(league_name: str, round: int, first: str, second: str, third: str, session: Session):
    _create_news(NewsType.EVENT_ENDED, [league_name, str(round), first, second, third], session)
    delete_news_with_type(NewsType.ONGOING_EVENT, session)


@transactional
def add_season_ended_news(league_name: str, winner: str, session: Session):
    _create_news(NewsType.SEASON_ENDED, [league_name, winner], session)


@transactional
def add_rookie_of_the_year_news(winner: str, session: Session):
    _create_news(NewsType.ROOKIE_OF_THE_YEAR, [winner], session)


@transactional
def add_new_season_news(season: int, transfers: dict[str, list[str]], retired: list[str], rookies: list[str], session: Session):
    """
    Creates a news record for the new starting season with the following data:
    - season: the number of the newly starting season
    - transfers: the list of leagues and the blobs transferred to the given season
    - retired: blobs that are retired from the championship system
    - rookies: new rookies that are starting their carreers
    """
    flattened_transfers_array: list[str] = []
    for (league, blobs) in transfers.items():
        flattened_transfers_array.append(league)
        flattened_transfers_array.append(str(len(blobs)))
        for blob in blobs:
            flattened_transfers_array.append(blob)

    _create_news(
        NewsType.NEW_SEASON,
        [
            str(season),
            str(len(transfers)),
            *flattened_transfers_array,
            str(len(retired)),
            *retired,
            str(len(rookies)),
            *rookies
        ],
        session
    )
    delete_old_news(session)


@transactional
def add_new_grandmaster_news(grandmaster: str, session: Session):
    _create_news(NewsType.NEW_GRANDMASTER, [grandmaster], session)


def _create_news(news_type: NewsType, data: list[str], session: Session):
    sim_date = get_sim_time(session)
    save_news(News(
        date=sim_date,
        news_type=news_type,
        news_data=data
    ), session)
