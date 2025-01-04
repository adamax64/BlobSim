import random
from typing import List

from data.db.db_engine import transactional
from data.model.blob import Blob
from data.persistence.blob_reposiotry import get_all_living_blobs, save_all_blobs, save_blob
from data.persistence.league_repository import get_queue
from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.enums.activity_type import ActivityType
from domain.sim_data_service import get_current_calendar, get_sim_time, reset_factory_progress
from domain.utils.activity_utils import choose_free_activity
from domain.utils.constants import (
    COMPETITION_EFFECT, CYCLES_PER_SEASON, INITIAL_INTEGRITY, LABOUR_SALARY,
    MAINTENANCE_COST, MAINTENANCE_EFFECT, PRACTICE_EFFECT
)


@transactional
def get_all_blobs(session) -> List[BlobStatsDto]:
    """ Get all living blobs and return them as a list of BlobStatsDto. """

    blobs: List[Blob] = get_all_living_blobs(session)
    return [BlobStatsDto(
        name=blob.name,
        born=blob.born,
        debut=blob.debut,
        contract=blob.contract,
        podiums=(blob.bronze_trophies + blob.silver_trophies + blob.gold_trophies),
        wins=blob.gold_trophies,
        championships=blob.championships,
        grandmasters=blob.grandmasters,
        league_name=blob.league.name if blob.league else 'None'
    ) for blob in blobs]


@transactional
def create_blob(session, name: str):
    """ Create a new blob with random stats and add it to the queue. """

    strength = 0.9 + random.random() * 0.2
    learning = 0.5 + 0.5 * random.random()
    current_time = get_sim_time(session)
    queue = get_queue(session)

    save_blob(session, Blob(
        name=name,
        strength=strength,
        learning=learning,
        integrity=INITIAL_INTEGRITY,
        born=current_time,
        league_id=queue.id
    ))
    reset_factory_progress(session)


@transactional
def update_blobs(session):
    """ Update all blobs living in the simulation and yield the progress in percentage. """

    current_event = get_current_calendar(session)
    current_event_league_id = current_event.league_id if current_event is not None else None
    blobs = get_all_living_blobs(session)

    current_time = get_sim_time(session)

    modified_blobs = []
    total_blobs = len(blobs)
    for index, blob in enumerate(blobs):
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

        yield int((index + 1) / total_blobs * 100)

    save_all_blobs(session, modified_blobs)


def _update_blob_strength(blob: Blob, multiplyer: float) -> float:
    """ Update the strength of the blob based on the activity multiplyer, its current integrity and learning. """

    atrophy = 0
    if blob.integrity < 0.4:
        tippingPoint = INITIAL_INTEGRITY * 0.6
        atrophy = -(blob.integrity - tippingPoint) / (1.2 * tippingPoint * CYCLES_PER_SEASON)

    return blob.strength - atrophy + multiplyer * blob.learning * (blob.integrity / INITIAL_INTEGRITY)


def _terminate_blob(blob: Blob, current_time: int):
    """ Terminate the blob if it's integrity or strength drops to or below zero. """

    if blob.integrity <= 0 or blob.strength <= 0:
        blob.league_id = None
        blob.terminated = current_time
