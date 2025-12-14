from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.event_type import EventType
from data.model.news import News
from data.model.news_type import NewsType
from data.persistence.news_repository import delete_news_with_type, delete_old_news, save_news
from domain.sim_data_service import get_sim_time


@transactional
def add_blob_created_news(blob_id: int, session: Session):
    # store blob ids as strings in the news_data array
    _create_news(NewsType.BLOB_CREATED, [str(blob_id)], session)
    delete_news_with_type(NewsType.BLOB_IN_CREATION, session)


@transactional
def add_blob_in_creation_news(session: Session):
    _create_news(NewsType.BLOB_IN_CREATION, [], session)


@transactional
def add_blob_terminated_news(blob_id: int, session: Session):
    _create_news(NewsType.BLOB_TERMINATED, [str(blob_id)], session)


@transactional
def add_event_starting_news(league_name: str, round: int, event_type: EventType, session: Session):
    _create_news(NewsType.EVENT_STARTED, [league_name, str(round), event_type.name], session)


@transactional
def add_ongoing_event_news(league_name: str, round: int, event_type: EventType, session: Session):
    _create_news(NewsType.ONGOING_EVENT, [league_name, str(round), event_type.name], session)
    delete_news_with_type(NewsType.EVENT_STARTED, session)


@transactional
def add_event_ended_news(league_name: str, round: int, event_id: int, session: Session):
    _create_news(NewsType.EVENT_ENDED, [league_name, str(round), str(event_id)], session)
    delete_news_with_type(NewsType.ONGOING_EVENT, session)


@transactional
def add_season_ended_news(league_name: str, winner_id: int, session: Session):
    _create_news(NewsType.SEASON_ENDED, [league_name, str(winner_id)], session)


@transactional
def add_rookie_of_the_year_news(winner_id: int, session: Session):
    _create_news(NewsType.ROOKIE_OF_THE_YEAR, [str(winner_id)], session)


@transactional
def add_new_season_news(season: int, transfers: dict[str, list[int]], retired: list[int], rookies: list[int], session: Session):
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
        for blob_id in blobs:
            flattened_transfers_array.append(str(blob_id))

    _create_news(
        NewsType.NEW_SEASON,
        [
            str(season),
            str(len(transfers)),
            *flattened_transfers_array,
            str(len(retired)),
            *[str(x) for x in retired],
            str(len(rookies)),
            *[str(x) for x in rookies]
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
