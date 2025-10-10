from dataclasses import dataclass
import random
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob import Blob
from data.model.calendar import Calendar
from data.model.event_type import EventType
from data.persistence.blob_reposiotry import (
    get_all_blobs_by_name,
    get_blob_by_id,
    save_all_blobs,
    save_blob,
    get_youngest_blob_debuting_in_season,
)
from domain.enums.activity_type import ActivityType
from domain.news_services.news_service import add_blob_terminated_news
from domain.sim_data_service import get_current_calendar, get_event_next_day, get_sim_time
from domain.standings_service import get_last_place_from_season_by_league
from data.persistence.league_repository import get_all_leagues_ordered_by_level
from data.persistence.result_repository import get_most_recent_real_league_result_of_blob
from domain.utils.sim_time_utils import get_season
from domain.utils.activity_utils import choose_activity
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
def update_all_blobs(session: Session):
    """Update all blobs living in the simulation and yield the progress in percentage."""

    current_event = get_current_calendar(session)
    event_next_day = get_event_next_day(session)

    blobs = get_all_blobs_by_name(session)

    catchup_training_blob_ids = (
        _collect_catchup_train_ids(session)
        if event_next_day is not None and event_next_day.event_type == EventType.CATCHUP_TRAINING
        else set()
    )

    current_time = get_sim_time(session)

    modified_blobs = []
    for blob in blobs:
        multiplyer = _proceed_with_activity(blob, current_event)

        _update_blob_stats(blob, multiplyer)
        blob.integrity -= 1
        _terminate_blob(blob, current_time, session)

        _choose_activity_for_blob(blob, event_next_day, catchup_training_blob_ids)

        modified_blobs.append(blob)

    save_all_blobs(session, modified_blobs)


@transactional
def update_blob_speed_by_id(blob_id: int, multiplyer: float, session: Session):
    blob = get_blob_by_id(session, blob_id)
    if blob:
        blob.speed = _update_stat(blob.speed, multiplyer, blob.learning, blob.integrity, 0)
        save_blob(session, blob)


def _proceed_with_activity(blob: Blob, current_event: Calendar | None) -> StatMultiplyers:
    multiplyer = StatMultiplyers(strength=0, speed=0)
    current_activity: ActivityType = blob.current_activity

    if current_activity == ActivityType.EVENT:
        if current_event.event_type == EventType.ENDURANCE_RACE:
            multiplyer.speed = COMPETITION_EFFECT
        elif current_event.event_type == EventType.ELIMINATION_SCORING:
            multiplyer.strength = COMPETITION_EFFECT
        else:
            multiplyer.strength = COMPETITION_EFFECT * 0.7
            multiplyer.speed = COMPETITION_EFFECT * 0.3
    elif current_activity == ActivityType.MAINTENANCE:
        if blob.money >= MAINTENANCE_COST:
            blob.money -= MAINTENANCE_COST
            blob.integrity += MAINTENANCE_EFFECT
    elif current_activity == ActivityType.LABOUR:
        blob.money += LABOUR_SALARY
    elif current_activity == ActivityType.PRACTICE:
        ratio = random.random()
        multiplyer.strength = PRACTICE_EFFECT * ratio
        multiplyer.speed = PRACTICE_EFFECT * (1 - ratio)
    elif current_activity == ActivityType.INTENSE_TRAINING:
        multiplyer.strength = PRACTICE_EFFECT * 1.1
        multiplyer.speed = PRACTICE_EFFECT * 1.1
    else:
        pass  # Idle activity

    return multiplyer


def _choose_activity_for_blob(
    blob: Blob,
    event_next_day: Calendar | None,
    catchup_training_blob_ids: set[int]
) -> ActivityType:
    """ Generate activity for blob for the next day """
    if blob.terminated is None:
        if blob.id in catchup_training_blob_ids:
            blob.current_activity = ActivityType.INTENSE_TRAINING
        elif event_next_day is not None and blob.league_id == event_next_day.league_id:
            blob.current_activity = ActivityType.EVENT
        else:
            extra_activities = []
            if blob.money >= MAINTENANCE_COST:
                extra_activities.append(ActivityType.MAINTENANCE)
            blob.current_activity = choose_activity(extra_activities)


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


def _terminate_blob(blob: Blob, current_time: int, session: Session):
    """Terminate the blob if it's integrity or any stat drops to or below zero."""
    if blob.integrity <= 0 or blob.strength <= 0 or blob.speed <= 0:
        blob.league_id = None
        blob.terminated = current_time
        add_blob_terminated_news(blob.id, session)


def _collect_catchup_train_ids(session: Session) -> set:
    """ Collect blob ids that should receive catch-up training. """
    train_ids: set[int] = set()

    current_season = get_season(get_sim_time(session))
    prev_season = current_season - 1

    youngest_debut = get_youngest_blob_debuting_in_season(session, current_season)
    if youngest_debut is not None:
        train_ids.add(youngest_debut.id)

    # from each real league, add last place blob from previous season standings
    leagues = get_all_leagues_ordered_by_level(session)
    for league in leagues:
        # skip dropout/queue league (level 0)
        if league.level == 0:
            continue
        last_place_id = get_last_place_from_season_by_league(league.id, prev_season, session)
        if last_place_id is not None:
            train_ids.add(last_place_id)

    # blobs that were demoted to the dropout league: present in dropout (level 0) but had a most recent real-league result elsewhere
    dropout_league = leagues[0] if leagues and leagues[0].level == 0 else None
    if dropout_league is not None:
        for b in dropout_league.players:
            recent = get_most_recent_real_league_result_of_blob(b.id, session)
            if recent is not None and int(recent.event.league.id) != dropout_league.id:
                train_ids.add(b.id)

    return train_ids
