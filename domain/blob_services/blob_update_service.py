from dataclasses import dataclass
from datetime import datetime
import random
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob import Blob
from data.model.calendar import Calendar
from data.model.event import Event
from data.model.event_type import EventType
from data.model.name_suggestion import NameSuggestion
from data.model.policy_type import PolicyType
from data.model.retirement_focus_type import RetirementFocusType
from data.model.trait import Trait
from data.persistence.blob_reposiotry import (
    get_all_blobs_by_name,
    get_blob_by_id,
    save_all_blobs,
    save_blob,
    get_youngest_blob_debuting_in_season,
)
from data.persistence.name_suggestion_repository import save_suggestion
from data.persistence.retirement_focus_repository import (
    remove_retirement_focus,
    set_retirement_focus,
)
from domain.enums.activity_type import ActivityType
from domain.hall_of_fame_services.titles_chronology_service import (
    get_current_grandmaster_id,
)
from domain.news_services.news_service import add_blob_terminated_news
from domain.sim_data_service import (
    get_event_next_day,
    get_sim_time,
)
from data.persistence.policy_repository import get_active_policy_by_type
from domain.policy_service import create_or_update_policy
from domain.standings_service import get_last_place_from_season_by_league, get_standings
from data.persistence.league_repository import (
    get_all_leagues_ordered_by_level,
    get_queue,
)
from data.persistence.result_repository import (
    get_most_recent_real_league_result_of_blob,
    has_dropout_results_from_last_season,
)
from data.persistence.event_repository import get_event_by_date
from data.persistence.action_repository import get_action_by_event_and_blob
from domain.event_record_services.race_event_records_service import (
    compute_sprint_finish_time,
)
from domain.utils.league_utils import get_race_duration_by_size
from domain.utils.blob_utils import has_state, has_trait, compute_state_multiplier
from domain.utils.policy_utils import choose_random_policy_type
from domain.utils.sim_time_utils import get_season
from domain.utils.activity_utils import choose_activity
from domain.item_service import grant_item_to_blob, is_inventory_full
from domain.utils.item_utils import choose_random_item_type
from domain.utils.constants import (
    COMPETITION_EFFECT,
    CYCLES_PER_SEASON,
    GRANDMASTER_SALARY,
    HEIR_COST,
    PREMIUM_PRACTICE_COST,
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

    event_next_day = get_event_next_day(session)

    blobs = get_all_blobs_by_name(session)

    catchup_training_blob_ids = (
        _collect_catchup_train_ids(session)
        if event_next_day is not None
        and event_next_day.event_type == EventType.CATCHUP_TRAINING
        else set()
    )

    current_time = get_sim_time(session)
    current_event = get_event_by_date(session, current_time)

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
            blob, event_next_day, catchup_training_blob_ids, is_grandmaster, session
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
    blob: Blob, current_event: Event | None, session: Session
) -> StatMultiplyers:
    multiplyer = StatMultiplyers(strength=0, speed=0)
    current_activity: ActivityType = blob.current_activity

    if current_activity == ActivityType.EVENT:
        if current_event.type == EventType.ENDURANCE_RACE:
            multiplyer.speed = COMPETITION_EFFECT
        elif current_event.type == EventType.SPRINT_RACE:
            multiplyer.speed = COMPETITION_EFFECT * _sprint_competition_time_multiplier(
                blob.id, current_event, session
            )
        elif current_event.type == EventType.ELIMINATION_SCORING:
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
        current_time = get_sim_time(session)
        practice_effect = _get_practice_effect(session)
        _reset_injured_state(blob, session, current_time)
        multiplyer = _practice_multiplyer(practice_effect, blob, session)
    elif current_activity == ActivityType.PREMIUM_PRACTICE:
        free = _is_premium_practice_free(blob, session)

        multiplier = 1.2 if has_state(blob, StateType.INJURED) else 1.6

        if free:
            practice_effect = _get_practice_effect(session, multiplier)
            multiplyer = _practice_multiplyer(practice_effect, blob, session)
        elif blob.money >= PREMIUM_PRACTICE_COST:
            blob.money -= PREMIUM_PRACTICE_COST
            practice_effect = _get_practice_effect(session, multiplier)
            multiplyer = _practice_multiplyer(practice_effect, blob, session)
        else:
            practice_effect = _get_practice_effect(session)
            multiplyer = _practice_multiplyer(practice_effect, blob, session)
    elif current_activity == ActivityType.INTENSE_PRACTICE:
        current_time = get_sim_time(session)
        practice_effect = _get_practice_effect(session, 1.7)
        multiplyer = _practice_multiplyer(practice_effect, blob, session)
        _refresh_tired_state(blob, current_time, session)
        _apply_intense_practice_state_changes(blob, session)
    elif current_activity == ActivityType.INTENSE_TRAINING:
        practice_effect = _get_practice_effect(session, 1.1)
        multiplyer = _practice_multiplyer(practice_effect, blob, session, ratio=False)
    elif current_activity == ActivityType.ADMINISTRATION:
        level = blob.grandmasters
        chosen = choose_random_policy_type()
        create_or_update_policy(session, chosen, level)
        blob.money += GRANDMASTER_SALARY
    elif current_activity == ActivityType.MINING:
        miners.append(blob)
    elif current_activity == ActivityType.APPLY_FOR_HEIR:
        if blob.money >= HEIR_COST:
            blob.money -= HEIR_COST
            # save name suggestion with parent id
            save_suggestion(
                session,
                NameSuggestion(
                    last_name=blob.last_name, parent_id=blob.id, created=datetime.now()
                ),
            )
            remove_retirement_focus(session, blob.id)
            if random.random() < 0.5:
                set_retirement_focus(
                    session, blob.id, RetirementFocusType.PROLONGED_LIFE
                )
    elif current_activity == ActivityType.ADVENTURE:
        if random.random() < 0.5:
            grant_item_to_blob(blob, choose_random_item_type(), session)
    else:
        pass  # Idle activity

    return multiplyer


def _is_premium_practice_free(blob: Blob, session: Session) -> bool:
    if blob.league and blob.league.level == 10:
        return True

    current_season = get_season(get_sim_time(session))
    if blob.contract == current_season and blob.league_id is not None:
        standings = get_standings(
            blob.league_id, current_season - 1, current_season, session
        )
        if standings:
            top_50_points_treshold = standings[-(len(standings) // 2)].total_points
            standings_by_blob = {standing.blob_id: standing for standing in standings}
            s = standings_by_blob.get(blob.id, None)
            if s is None or s.total_points <= top_50_points_treshold:
                return True

    return False


def _get_practice_effect(session: Session, multiplier: float = 1.0) -> float:
    current_time = get_sim_time(session)
    gym_improvement_level = get_active_policy_by_type(
        session, PolicyType.GYM_IMPROVEMENT, current_time
    )
    practice_effect = PRACTICE_EFFECT * multiplier
    if gym_improvement_level:
        practice_effect += practice_effect * (
            0.05 * gym_improvement_level.applied_level
        )
    return practice_effect


def _practice_multiplyer(
    practice_effect: float, blob: Blob, session: Session, ratio: bool = True
) -> StatMultiplyers:
    current_time = get_sim_time(session)
    state_multiplier = compute_state_multiplier(blob, current_time)
    if ratio:
        split = random.random()
        return StatMultiplyers(
            strength=practice_effect * split * state_multiplier,
            speed=practice_effect * (1 - split) * state_multiplier,
        )
    return StatMultiplyers(
        strength=practice_effect * state_multiplier,
        speed=practice_effect * state_multiplier,
    )


def _reset_injured_state(blob: Blob, session: Session, current_time: int):
    for st in blob.states:
        if st.type == StateType.INJURED and st.effect_until >= current_time:
            if random.random() < 0.15:
                st.effect_until = current_time + 4
                try:
                    save_state(session, st)
                except Exception:
                    pass


def _refresh_tired_state(blob: Blob, current_time: int, session: Session):
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


def _apply_intense_practice_state_changes(blob: Blob, session: Session):
    determined = has_trait(blob, TraitType.DETERMINED)
    tired_chance = 0.4 if not determined else 0.2
    injured_chance = 0.1 if not determined else 0.05

    if random.random() < tired_chance:
        if has_state(blob, StateType.TIRED):
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
        if random.random() < max(0, (1 - blob.integrity / INITIAL_INTEGRITY) * 0.2):
            blob.integrity -= 1
        create_state(session, blob.id, StateType.INJURED, effect_until)


def _sprint_competition_time_multiplier(
    blob_id: int, event: Event | None, session: Session
) -> float:
    """Scale competition effect by finish time relative to max race distance (ticks)."""
    if event is None:
        return 1.0

    action = get_action_by_event_and_blob(session, event.id, blob_id)
    if action is None or not action.scores:
        return 1.0

    previous_distance = sum(action.scores)
    score = action.scores[-1]
    race_length = get_race_duration_by_size(len(event.actions))
    if previous_distance + score <= race_length:
        return 1.0

    tick = len(action.scores) - 1
    finish_time = compute_sprint_finish_time(
        previous_distance, score, tick, race_length
    )
    return finish_time / race_length


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
    - LAZY cannot coexist with HARD_WORKING, ADVENTUROUS or DETERMINED
    """
    threshold = INITIAL_INTEGRITY - CYCLES_PER_SEASON * 2

    if blob.integrity > threshold:
        if random.random() < 0.001:
            # Currently the LAZY trait counters every other trait so it can only be lost
            # If this changes, the LAZY condition should be removed
            if blob.traits and (has_trait(blob, TraitType.LAZY) or len(blob.traits) == 3):
                lost_trait = random.choice(blob.traits)
                delete_trait(session, lost_trait.id)
                session.refresh(blob)

            if random.random() < 0.5 and blob.traits and len(blob.traits) > 0:
                lost_trait = random.choice(blob.traits)
                delete_trait(session, lost_trait.id)
                session.refresh(blob)
            else:
                available_traits = [t for t in TraitType if not has_trait(blob, t)]

                # Filter out conflicting traits
                has_lazy = has_trait(blob, TraitType.LAZY)
                has_hardworking = has_trait(blob, TraitType.HARD_WORKING)
                has_determined = has_trait(blob, TraitType.DETERMINED)
                has_adventorous = has_trait(blob, TraitType.ADVENTUROUS)

                if has_lazy:
                    # Remove HARD_WORKING and DETERMINED if blob has LAZY
                    available_traits = [
                        t
                        for t in available_traits
                        if t not in (TraitType.HARD_WORKING, TraitType.DETERMINED, TraitType.ADVENTUROUS)
                    ]
                elif has_hardworking or has_determined or has_adventorous:
                    # Remove LAZY if blob has HARD_WORKING or DETERMINED
                    available_traits = [
                        t for t in available_traits if t != TraitType.LAZY
                    ]

                if len(available_traits) > 0:
                    new_trait = random.choice(available_traits)
                    save_trait(session, Trait(blob_id=blob.id, type=new_trait))
                    session.refresh(blob)


def _choose_activity_for_blob(
    blob: Blob,
    event_next_day: Calendar | None,
    catchup_training_blob_ids: set[int],
    is_grandmaster: bool,
    session: Session,
) -> ActivityType:
    """Generate activity for blob for the next day"""
    if blob.terminated is None:
        if blob.id in catchup_training_blob_ids:
            blob.current_activity = ActivityType.INTENSE_TRAINING
        elif (
            event_next_day is not None
            and event_next_day.league_id is not None
            and blob.league_id == event_next_day.league_id
        ):
            blob.current_activity = ActivityType.EVENT
        else:
            extra_activities = []
            if blob.money >= MAINTENANCE_COST and (
                blob.retirement_focus is None
                or blob.retirement_focus.focus_type != RetirementFocusType.LEGACY
            ):
                extra_activities.append(ActivityType.MAINTENANCE)

            free_premium_practice = None
            if blob.league and blob.league.level == 10:
                free_premium_practice = True
            elif blob.contract is not None and blob.contract >= get_season(
                get_sim_time(session)
            ):
                free_premium_practice = _is_premium_practice_free(blob, session)
                if free_premium_practice or blob.money >= PREMIUM_PRACTICE_COST:
                    extra_activities.append(ActivityType.PREMIUM_PRACTICE)

            if blob.money >= HEIR_COST:
                extra_activities.append(ActivityType.APPLY_FOR_HEIR)

            # grandmasters may enact policies
            if is_grandmaster:
                extra_activities.append(ActivityType.ADMINISTRATION)

            blob.current_activity = choose_activity(
                blob,
                extra_activities,
                free_premium_practice,
                adventure_blocked=is_inventory_full(blob, session),
            )


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
        # skip queue league (level 10)
        if league.level == 10:
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
            was_in_dropout_before = has_dropout_results_from_last_season(b.id, session)
            if (
                recent is not None
                and int(recent.event.league.id) != dropout_league.id
                and not was_in_dropout_before
            ):
                train_ids.add(b.id)

    # blobs on queue who born before the current season
    queue = get_queue(session)
    if queue is not None:
        for blob in queue.players:
            if get_season(blob.born) < current_season:
                train_ids.add(blob.id)

    # blobs who has ending contract and finished outside the top 50% last season
    for league in leagues:
        if league.level == 10:
            continue
        blobs_in_danger = filter(lambda x: x.contract == current_season, league.players)
        standings = get_standings(
            league.id, current_season - 1, current_season, session
        )
        top_50_points_treshold = standings[-(len(standings) // 2)].total_points
        standings_by_blob = {standing.blob_id: standing for standing in standings}
        for blob in blobs_in_danger:
            standings = standings_by_blob.get(blob.id, None)
            if standings is None or standings.total_points <= top_50_points_treshold:
                train_ids.add(blob.id)

    return train_ids
