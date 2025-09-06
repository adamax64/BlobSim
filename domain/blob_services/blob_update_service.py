from dataclasses import dataclass
import random
from data.db.db_engine import transactional
from data.model.blob import Blob
from data.model.event_type import EventType
from data.persistence.blob_reposiotry import get_all_blobs_by_name, get_blob_by_id, save_all_blobs, save_blob
from domain.enums.activity_type import ActivityType
from domain.sim_data_service import get_current_calendar, get_sim_time
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


@dataclass
class StatMultiplyers:
    strength: float
    speed: float


@transactional
def update_all_blobs(session):
    """Update all blobs living in the simulation and yield the progress in percentage."""

    current_event = get_current_calendar(session)
    blobs = get_all_blobs_by_name(session)

    current_time = get_sim_time(session)

    modified_blobs = []
    for blob in blobs:
        multiplyer = StatMultiplyers(strength=0, speed=0)
        if blob.league_id == current_event.league_id if current_event is not None else None:
            if current_event.event_type == EventType.ENDURANCE_RACE:
                multiplyer.speed = COMPETITION_EFFECT
            elif current_event.event_type == EventType.ELIMINATION_SCORING:
                multiplyer.strength = COMPETITION_EFFECT
            else:
                multiplyer.strength = COMPETITION_EFFECT * 0.7
                multiplyer.speed = COMPETITION_EFFECT * 0.3
        elif blob.money >= MAINTENANCE_COST and random.random() < 0.5:
            blob.money -= MAINTENANCE_COST
            blob.integrity += MAINTENANCE_EFFECT
        else:
            activity = choose_free_activity()
            if activity == ActivityType.LABOUR:
                blob.money += LABOUR_SALARY
            elif activity == ActivityType.PRACTICE:
                ratio = random.random()
                multiplyer.strength = PRACTICE_EFFECT * ratio
                multiplyer.speed = PRACTICE_EFFECT * (1 - ratio)
        _update_blob_stats(blob, multiplyer)
        blob.integrity -= 1
        _terminate_blob(blob, current_time)

        modified_blobs.append(blob)

    save_all_blobs(session, modified_blobs)


@transactional
def update_blob_speed_by_id(blob_id: int, multiplyer: float, session):
    blob = get_blob_by_id(session, blob_id)
    if blob:
        blob.speed = _update_stat(blob.speed, multiplyer, blob.learning, blob.integrity, 0)
        save_blob(session, blob)


def _update_blob_stats(blob: Blob, multiplyer: StatMultiplyers):
    """Update the stats of the blob based on the activity multiplyer, its current integrity and learning."""

    atrophy = 0
    if blob.integrity < INITIAL_INTEGRITY * 0.4:
        tippingPoint = INITIAL_INTEGRITY * 0.6
        atrophy = -(blob.integrity - tippingPoint) / (
            1.2 * tippingPoint * CYCLES_PER_SEASON
        )

    blob.strength = _update_stat(blob.strength, multiplyer.strength, blob.learning, blob.integrity, atrophy)
    blob.speed = _update_stat(blob.speed, multiplyer.speed, blob.learning, blob.integrity, atrophy)


def _update_stat(stat: float, multiplyer: float, learning: float, integrity: float, atrophy: float) -> float:
    """Update the stat of the blob based on the activity multiplyer."""

    return stat - atrophy + multiplyer * learning * (integrity / INITIAL_INTEGRITY)


def _terminate_blob(blob: Blob, current_time: int):
    """Terminate the blob if it's integrity or any stat drops to or below zero."""

    if blob.integrity <= 0 or blob.strength <= 0 or blob.speed <= 0:
        blob.league_id = None
        blob.terminated = current_time
