from dataclasses import dataclass
import random
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob import Blob
from data.model.calendar import Calendar
from data.model.event_type import EventType
from data.model.policy_type import PolicyType
from data.persistence.blob_reposiotry import (
    get_all_blobs_by_name,
    get_blob_by_id,
    save_all_blobs,
    save_blob,
    get_youngest_blob_debuting_in_season,
)
from domain.enums.activity_type import ActivityType
from domain.hall_of_fame_services.titles_chronology_service import (
    get_current_grandmaster_id,
)
from domain.news_services.news_service import add_blob_terminated_news
from domain.sim_data_service import (
    get_current_calendar,
    get_event_next_day,
    get_sim_time,
)
from data.persistence.policy_repository import get_active_policy_by_type
from domain.policy_service import create_or_update_policy
from domain.standings_service import get_last_place_from_season_by_league
from data.persistence.league_repository import get_all_leagues_ordered_by_level
from data.persistence.result_repository import (
    get_most_recent_real_league_result_of_blob,
)
from domain.utils.blob_utils import has_state, has_trait, compute_state_multiplier
from domain.utils.policy_utils import choose_random_policy_type
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
from data.persistence.state_repository import create_state, save_state
from data.persistence.trait_repository import delete_trait, save_trait
from data.model.trait_type import TraitType
from data.model.state_type import StateType

miners: list[Blob] = []


@dataclass
class StatMultiplyers:
    strength: float
    speed: float


@transactional
def update_all_blobs(session: Session):
    global miners
    """Update all blobs living in the simulation and yield the progress in percentage."""

    current_event = get_current_calendar(session)
    event_next_day = get_event_next_day(session)

    blobs = get_all_blobs_by_name(session)

    catchup_training_blob_ids = (
        _collect_catchup_train_ids(session)
        if event_next_day is not None
        and event_next_day.event_type == EventType.CATCHUP_TRAINING
        else set()
    )

    current_time = get_sim_time(session)

    modified_blobs = []
    miners = []
    for blob in blobs:
        multiplyer = _proceed_with_activity(blob, current_event, session)

        _update_blob_stats(blob, multiplyer)
        blob.integrity -= 1
        _terminate_blob(blob, current_time, session)

        is_grandmaster = get_current_grandmaster_id(session) == blob.id
        _apply_random_states(blob, session)
        _apply_random_traits(blob, session)
        _choose_activity_for_blob(
            blob, event_next_day, catchup_training_blob_ids, is_grandmaster
        )

        modified_blobs.append(blob)

    # Distribute mining reward: pick one miner and give them money equal to number of miners
    if miners:
        chosen = random.choice(miners)
        reward = len(miners)
        chosen.money += reward
        print(f"[INFO] Blob {chosen.id} received mining reward of {reward} coins.")

        # Ensure the chosen blob is included in saved blobs
        if chosen not in modified_blobs:
            modified_blobs.append(chosen)

    save_all_blobs(session, modified_blobs)


@transactional
def update_blob_speed_by_id(blob_id: int, multiplyer: float, session: Session):
    blob = get_blob_by_id(session, blob_id)
    if blob:
        blob.speed = _update_stat(
            blob.speed, multiplyer, blob.learning, blob.integrity, 0
        )
        save_blob(session, blob)


def _proceed_with_activity(
    blob: Blob, current_event: Calendar | None, session: Session
) -> StatMultiplyers:
    global miners

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
        # base labour salary
        blob.money += LABOUR_SALARY

        # apply active salary raise policies
        current_time = get_sim_time(session)
        labour_subsidies = get_active_policy_by_type(
            session, PolicyType.LABOUR_SUBSIDIES, current_time
        )
        if labour_subsidies:
            blob.money += 1

            chance = 0.1 * (labour_subsidies.applied_level - 1)
            if chance > 1:
                chance = 1
            if random.random() < chance:
                blob.money += 1
        # small chance to refresh TIRED state cooldown during labour
        current_time = get_sim_time(session)
        for st in blob.states:
            if st.type == StateType.TIRED and st.effect_until >= current_time:
                if random.random() < 0.05:
                    st.effect_until = current_time + 2
                    try:
                        save_state(session, st)
                    except Exception:
                        pass
    elif current_activity == ActivityType.PRACTICE:
        ratio = random.random()
        current_time = get_sim_time(session)
        gym_improvement_level = get_active_policy_by_type(
            session, PolicyType.GYM_IMPROVEMENT, current_time
        )
        practice_effect = PRACTICE_EFFECT
        if gym_improvement_level:
            practice_effect += practice_effect * (
                0.05 * gym_improvement_level.applied_level
            )
        current_time = get_sim_time(session)
        state_multiplier = compute_state_multiplier(blob, current_time)

        # injured state has a 15% chance to reset its cooldown (refresh duration)
        for st in blob.states:
            if st.type == StateType.INJURED and st.effect_until >= current_time:
                if random.random() < 0.15:
                    # refresh injured duration to 4 days from now
                    st.effect_until = current_time + 4
                    try:
                        save_state(session, st)
                    except Exception:
                        pass
        multiplyer.strength = practice_effect * ratio * state_multiplier
        multiplyer.speed = practice_effect * (1 - ratio) * state_multiplier
    elif current_activity == ActivityType.INTENSE_PRACTICE:
        ratio = random.random()
        current_time = get_sim_time(session)
        gym_improvement_level = get_active_policy_by_type(
            session, PolicyType.GYM_IMPROVEMENT, current_time
        )
        practice_effect = PRACTICE_EFFECT * 1.7
        if gym_improvement_level:
            practice_effect += practice_effect * (
                0.05 * gym_improvement_level.applied_level
            )
        current_time = get_sim_time(session)
        state_multiplier = compute_state_multiplier(blob, current_time)
        multiplyer.strength = practice_effect * ratio * state_multiplier
        multiplyer.speed = practice_effect * (1 - ratio) * state_multiplier
        # small chance to refresh TIRED state cooldown during practice
        for st in blob.states:
            if (
                st.type == StateType.TIRED
                and getattr(st, "effect_until", 0) >= current_time
            ):
                if random.random() < 0.05:
                    st.effect_until = current_time + 2
                    try:
                        save_state(session, st)
                    except Exception:
                        pass

        # chance to gain states from intense practice
        determined = has_trait(blob, TraitType.DETERMINED)
        tired_chance = 0.4 if not determined else 0.2
        injured_chance = 0.1 if not determined else 0.05

        if random.random() < tired_chance:
            if has_state(blob, StateType.TIRED):
                # if already tired, extend tired duration by 2 days
                current_time = get_sim_time(session)
                for st in blob.states:
                    if st.type == StateType.TIRED and st.effect_until >= current_time:
                        st.effect_until += 2
                        try:
                            save_state(session, st)
                        except Exception:
                            pass
            else:
                effect_until = get_sim_time(session) + 2
                create_state(session, blob.id, StateType.TIRED, effect_until)

        if random.random() < injured_chance:
            effect_until = get_sim_time(session) + 4
            create_state(session, blob.id, StateType.INJURED, effect_until)
    elif current_activity == ActivityType.INTENSE_TRAINING:
        practice_effect = PRACTICE_EFFECT * 1.1
        current_time = get_sim_time(session)
        gym_improvement_level = get_active_policy_by_type(
            session, PolicyType.GYM_IMPROVEMENT, current_time
        )
        if gym_improvement_level:
            practice_effect += practice_effect * (
                0.05 * gym_improvement_level.applied_level
            )

        current_time = get_sim_time(session)
        state_multiplier = compute_state_multiplier(blob, current_time)
        multiplyer.strength = practice_effect * state_multiplier
        multiplyer.speed = practice_effect * state_multiplier
    elif current_activity == ActivityType.ADMINISTRATION:
        level = blob.grandmasters
        chosen = choose_random_policy_type()
        create_or_update_policy(session, chosen, level)
        blob.money += 2  # grandmaster salary
    elif current_activity == ActivityType.MINING:
        miners.append(blob)
    else:
        pass  # Idle activity

    return multiplyer


def _apply_random_states(blob: Blob, session: Session):
    """Apply random state generation: 1% chance for GLOOMY and 1% chance for FOCUSED if not already present."""
    current_time = get_sim_time(session)

    if not has_state(blob, StateType.GLOOMY) and not has_state(blob, StateType.FOCUSED):
        random_value = random.random()
        if random_value < 0.01:
            effect_until = current_time + 1
            create_state(session, blob.id, StateType.GLOOMY, effect_until)
        elif random.random() < 0.02:
            effect_until = current_time + 1
            create_state(session, blob.id, StateType.FOCUSED, effect_until)
        session.refresh(blob)  # Refresh blob to get the latest states after creation


def _apply_random_traits(blob: Blob, session: Session):
    """Apply random trait changes: if integrity is high, 0.1% chance to either gain or lose a trait.

    Trait conflict rules:
    - LAZY cannot coexist with HARD_WORKING or DETERMINED
    """
    threshold = INITIAL_INTEGRITY - CYCLES_PER_SEASON * 2

    if blob.integrity > threshold:
        if random.random() < 0.001:
            if random.random() < 0.5:
                if blob.traits and len(blob.traits) > 0:
                    lost_trait = random.choice(blob.traits)
                    delete_trait(session, lost_trait.id)
                    session.refresh(blob)
            else:
                available_traits = [t for t in TraitType if not has_trait(blob, t)]

                # Filter out conflicting traits
                has_lazy = has_trait(blob, TraitType.LAZY)
                has_hardworking = has_trait(blob, TraitType.HARD_WORKING)
                has_determined = has_trait(blob, TraitType.DETERMINED)

                if has_lazy:
                    # Remove HARD_WORKING and DETERMINED if blob has LAZY
                    available_traits = [
                        t
                        for t in available_traits
                        if t not in (TraitType.HARD_WORKING, TraitType.DETERMINED)
                    ]
                elif has_hardworking or has_determined:
                    # Remove LAZY if blob has HARD_WORKING or DETERMINED
                    available_traits = [
                        t for t in available_traits if t != TraitType.LAZY
                    ]

                if len(available_traits) > 0:
                    new_trait = random.choice(available_traits)
                    save_trait(session, blob.id, new_trait)
                    session.refresh(blob)


def _choose_activity_for_blob(
    blob: Blob,
    event_next_day: Calendar | None,
    catchup_training_blob_ids: set[int],
    is_grandmaster: bool,
) -> ActivityType:
    """Generate activity for blob for the next day"""
    if blob.terminated is None:
        if blob.id in catchup_training_blob_ids:
            blob.current_activity = ActivityType.INTENSE_TRAINING
        elif event_next_day is not None and blob.league_id == event_next_day.league_id:
            blob.current_activity = ActivityType.EVENT
        else:
            extra_activities = []
            if blob.money >= MAINTENANCE_COST:
                extra_activities.append(ActivityType.MAINTENANCE)
            # grandmasters may enact policies
            if is_grandmaster:
                extra_activities.append(ActivityType.ADMINISTRATION)
            blob.current_activity = choose_activity(blob, extra_activities)


def _update_blob_stats(blob: Blob, multiplyer: StatMultiplyers):
    """Update the stats of the blob based on the activity multiplyer, its current integrity and learning."""

    atrophy = 0
    if blob.integrity < INITIAL_INTEGRITY * 0.4:
        tippingPoint = INITIAL_INTEGRITY * 0.6
        atrophy = -(blob.integrity - tippingPoint) / (
            1.2 * tippingPoint * CYCLES_PER_SEASON
        )

    blob.strength = _update_stat(
        blob.strength, multiplyer.strength, blob.learning, blob.integrity, atrophy
    )
    blob.speed = _update_stat(
        blob.speed, multiplyer.speed, blob.learning, blob.integrity, atrophy
    )


def _update_stat(
    stat: float, multiplyer: float, learning: float, integrity: float, atrophy: float
) -> float:
    """Update the stat of the blob based on the activity multiplyer."""

    return stat - atrophy + multiplyer * learning * (integrity / INITIAL_INTEGRITY)


def _terminate_blob(blob: Blob, current_time: int, session: Session):
    """Terminate the blob if it's integrity or any stat drops to or below zero."""
    if blob.integrity <= 0 or blob.strength <= 0 or blob.speed <= 0:
        blob.league_id = None
        blob.terminated = current_time
        add_blob_terminated_news(blob.id, session)


def _collect_catchup_train_ids(session: Session) -> set:
    """Collect blob ids that should receive catch-up training."""
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
        last_place_id = get_last_place_from_season_by_league(
            league.id, prev_season, session
        )
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
