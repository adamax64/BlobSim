from logging import warning
import random
from sqlalchemy.exc import IntegrityError

from data.db.db_engine import transactional
from data.model.blob import Blob
from data.persistence.blob_reposiotry import (
    get_all_blobs_by_name,
    get_blob_by_id,
    save_all_blobs,
    save_blob,
)
from data.persistence.league_repository import get_queue
from data.persistence.name_suggestion_repository import (
    delete_suggestion,
    get_oldest_name,
)
from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.enums.activity_type import ActivityType
from domain.exceptions.name_occupied_exception import NameOccupiedException
from domain.sim_data_service import (
    get_current_calendar,
    get_sim_time,
    is_blob_created,
    reset_factory_progress,
)
from domain.utils.activity_utils import choose_free_activity
from domain.utils.constants import (
    COMPETITION_EFFECT,
    CYCLES_PER_SEASON,
    INITIAL_INTEGRITY,
    LABOUR_SALARY,
    MAINTENANCE_COST,
    MAINTENANCE_EFFECT,
    PRACTICE_EFFECT,
)
from domain.utils.sim_time_utils import format_sim_time_short, get_season


@transactional
def get_all_blobs(
    session, name_search: str = None, show_dead: bool = False
) -> list[BlobStatsDto]:
    """Get all living blobs and return them as a list of BlobStatsDto."""

    blobs: list[Blob] = get_all_blobs_by_name(
        session=session, name_search=name_search, show_dead=show_dead
    )

    current_season = get_season(get_sim_time(session))

    return [
        BlobStatsDto(
            name=f"{blob.first_name} {blob.last_name}",
            born=format_sim_time_short(blob.born),
            debut=blob.debut,
            contract=blob.contract,
            podiums=(blob.bronze_trophies + blob.silver_trophies + blob.gold_trophies),
            wins=blob.gold_trophies,
            championships=blob.championships,
            grandmasters=blob.grandmasters,
            league_name=blob.league.name if blob.league else "None",
            at_risk=blob.contract == current_season,
            is_dead=blob.terminated is not None,
            is_retired=blob.contract is not None and blob.contract < current_season,
        )
        for blob in blobs
    ]


@transactional
def check_blob_created(session) -> str | bool:
    if is_blob_created(session):
        return _create_with_name_suggestion(session)
    return False


@transactional
def create_blob(session, first_name: str, last_name: str, parent_id: int | None = None):
    """Create a new blob with random stats and add it to the queue."""

    strength = 0.9 + random.random() * 0.2
    learning = 0.5 + 0.5 * random.random()
    current_time = get_sim_time(session)
    queue = get_queue(session)

    if parent_id is not None:
        parent = get_blob_by_id(session, parent_id)
        learning += parent.championships * 0.01
        strength += parent.grandmasters * 0.01

    try:
        save_blob(
            session,
            Blob(
                first_name=first_name,
                last_name=last_name,
                strength=strength,
                learning=learning,
                integrity=INITIAL_INTEGRITY,
                born=current_time,
                league_id=queue.id,
                parent_id=parent_id,
            ),
        )
        reset_factory_progress(session)
    except IntegrityError:
        raise NameOccupiedException()


@transactional
def update_blobs(session):
    """Update all blobs living in the simulation and yield the progress in percentage."""

    current_event = get_current_calendar(session)
    current_event_league_id = (
        current_event.league_id if current_event is not None else None
    )
    blobs = get_all_blobs_by_name(session)

    current_time = get_sim_time(session)

    modified_blobs = []
    for blob in blobs:
        multiplyer = 0
        if blob.league_id == current_event_league_id:
            multiplyer = COMPETITION_EFFECT
        elif blob.money >= MAINTENANCE_COST and random.random() < 0.5:
            blob.money -= MAINTENANCE_COST
            blob.integrity += MAINTENANCE_EFFECT
        else:
            activity = choose_free_activity()
            if activity == ActivityType.LABOUR:
                blob.money += LABOUR_SALARY
            elif activity == ActivityType.PRACTICE:
                multiplyer = PRACTICE_EFFECT
        blob.strength = _update_blob_strength(blob, multiplyer)
        blob.integrity -= 1
        _terminate_blob(blob, current_time)

        modified_blobs.append(blob)

    save_all_blobs(session, modified_blobs)


def _update_blob_strength(blob: Blob, multiplyer: float) -> float:
    """Update the strength of the blob based on the activity multiplyer, its current integrity and learning."""

    atrophy = 0
    if blob.integrity < 0.4:
        tippingPoint = INITIAL_INTEGRITY * 0.6
        atrophy = -(blob.integrity - tippingPoint) / (
            1.2 * tippingPoint * CYCLES_PER_SEASON
        )

    return (
        blob.strength
        - atrophy
        + multiplyer * blob.learning * (blob.integrity / INITIAL_INTEGRITY)
    )


@transactional
def _create_with_name_suggestion(session) -> str | bool:
    """Try to create new blob with suggested names. Retry if there is already a blob with suggested name"""

    name_suggestion = get_oldest_name(session)
    if name_suggestion is None:
        return True
    try:
        create_blob(session, name_suggestion.name)
        delete_suggestion(session, name_suggestion)
        return name_suggestion.name
    except NameOccupiedException:
        session.close()
        warning("There already exists a blob with suggested name, retrying creating blob...")
        delete_suggestion(name=name_suggestion)
        return _create_with_name_suggestion()


def _terminate_blob(blob: Blob, current_time: int):
    """Terminate the blob if it's integrity or strength drops to or below zero."""

    if blob.integrity <= 0 or blob.strength <= 0:
        blob.league_id = None
        blob.terminated = current_time
