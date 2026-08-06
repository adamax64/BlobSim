from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob import Blob
from data.persistence.blob_repository import (
    get_all_blobs_by_name,
    get_blob_by_id,
    get_by_activities,
)
from data.persistence.event_repository import get_event_by_id
from domain.dtos.blob_dtos.blob_stats_dto import BlobStatsDto
from domain.enums.activity_type import ActivityType
from domain.exceptions.no_grandmaster_found_exception import NoGrandmasterFoundException
from domain.hall_of_fame_services.titles_chronology_service import (
    get_current_grandmaster_id,
)
from domain.sim_data_service import get_sim_time
from domain.standings_service import (
    get_last_season_standings_position,
    get_standings,
    get_standings_by_league,
)
from domain.utils.blob_utils import map_to_blob_state_dto
from domain.utils.sim_time_utils import get_season


@transactional
def fetch_all_blobs(
    session: Session, name_search: str = None, show_dead: bool = False
) -> list[BlobStatsDto]:
    """Get all living blobs and return them as a list of BlobStatsDto."""

    blobs: list[Blob] = get_all_blobs_by_name(
        session=session, name_search=name_search, show_dead=show_dead
    )

    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)

    # Fetch standings to get positions
    standings_by_league = get_standings_by_league(session, blobs, current_season)

    return [
        map_to_blob_state_dto(
            blob,
            current_season,
            grandmaster_id,
            standings_position=(
                standings_by_league.get(blob.league_id).get(blob.id)
                if blob.league_id
                else None
            ),
        )
        for blob in blobs
    ]


@transactional
def fetch_blob_by_id(
    blob_id: int, session: Session, event_id: int | None = None
) -> BlobStatsDto:
    """Fetch a blob by its ID and return it as a BlobStatsDto.

    If `event_id` is given, the blob's standings position reflects the state as of that event
    (i.e. truncated to the event's round, in the event's season) instead of the current standings.
    """

    current_season = get_season(get_sim_time(session))
    blob = get_blob_by_id(session, blob_id)
    grandmaster_id = get_current_grandmaster_id(session)

    if not blob:
        raise ValueError(f"Blob with ID {blob_id} not found")

    event = get_event_by_id(session, event_id) if event_id is not None else None
    standings_season = event.season if event is not None else current_season
    through_round = event.round - 1 if event is not None else None

    league_id = event.league_id if event is not None else blob.league.id if blob.league else None

    # Fetch standings position
    standings_position = None
    last_season_standings_position = None
    if blob.league:
        standings = get_standings(
            session=session,
            league_id=league_id,
            season=standings_season,
            current_season=standings_season,
            through_round=through_round,
        )
        for idx, standing in enumerate(standings):
            if standing.blob_id == blob_id:
                standings_position = idx + 1
                break

        if standings_position is None or (through_round is not None and through_round == 0):
            last_season_standings_position = get_last_season_standings_position(
                session=session,
                league_id=league_id,
                blob_id=blob_id,
                season=standings_season,
            )

    return map_to_blob_state_dto(
        blob,
        standings_season,
        grandmaster_id,
        standings_position=standings_position,
        last_season_standings_position=last_season_standings_position,
    )


@transactional
def get_current_grandmaster(session: Session) -> BlobStatsDto:
    """Fetch the current grandmaster blob and return it as a BlobStatsDto."""
    grandmaster_id = get_current_grandmaster_id(session)
    if not grandmaster_id:
        raise NoGrandmasterFoundException()
    return fetch_blob_by_id(grandmaster_id, session)


@transactional
def get_blobs_by_activities(
    session: Session, activities: list[ActivityType]
) -> list[BlobStatsDto]:
    """Fetch all blobs that currently does one of the activities specified."""
    blobs: list[Blob] = get_by_activities(session=session, activities=activities)

    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)

    # Fetch standings to get positions
    standings_by_league = get_standings_by_league(session, blobs, current_season)

    return [
        map_to_blob_state_dto(
            blob,
            current_season,
            grandmaster_id,
            standings_position=(
                standings_by_league.get(blob.league_id).get(blob.id)
                if blob.league_id
                else None
            ),
        )
        for blob in blobs
    ]
