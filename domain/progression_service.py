import random
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.policy_type import PolicyType
from data.persistence.calendar_repository import get_calendar
from data.persistence.sim_data_repository import get_sim_data, save_sim_data
from domain.blob_services.blob_creation_service import check_factory_and_create_blob
from data.persistence.policy_repository import get_active_policy_by_type
from data.persistence.blob_reposiotry import get_all_retired, save_all_blobs
from domain.calendar_service import recreate_calendar_for_next_season
from domain.league_service import manage_league_transfers
from domain.news_services.news_service import add_event_starting_news, add_new_grandmaster_news
from domain.sim_data_service import is_unconcluded_event_today
from domain.standings_service import get_grandmaster_standings
from domain.utils.sim_time_utils import get_season, is_season_end


@transactional
def progress_simulation(session: Session):
    """
    Advances the simulation by one time unit, updating simulation data and handling season transitions.
    This function performs the following steps:
    1. Checks if the current simulation time marks the end of a season.
       - If so, manages league transfers and recreates the calendar for the next season.
    2. Progresses blob factory production by a random amount between 1 and 5.
    3. Increments the simulation time by one unit.
    4. If there is an unconcluded event scheduled for today:
       - Adds a news entry about the starting event, including the league name, round, and event type.
    """

    sim_data = get_sim_data(session)
    if is_season_end(sim_data.sim_time):
        manage_league_transfers(session, get_season(sim_data.sim_time))
        recreate_calendar_for_next_season(session, get_season(sim_data.sim_time) + 1)
        _inagruate_grandmaster(get_season(sim_data.sim_time), session)

    # base factory progress plus any active factory modernization policies
    extra = 0
    factory_level = get_active_policy_by_type(session, PolicyType.FACTORY_MODERNIZATION, sim_data.sim_time)
    if factory_level:
        extra = factory_level.applied_level
    sim_data.factory_progress += random.randint(1, 5) + extra
    sim_data.sim_time += 1
    save_sim_data(session, sim_data)

    _hand_out_pensions(session, sim_data.sim_time)

    _check_and_add_event_news(sim_data.sim_time, session)
    check_factory_and_create_blob(session)


def _inagruate_grandmaster(current_season: int, session: Session):
    if current_season % 4 == 0:
        standings = get_grandmaster_standings(current_season - 3, current_season, session)
        grandmaster = standings[0]
        add_new_grandmaster_news(grandmaster.blob_id, session)


def _check_and_add_event_news(sim_time: int, session: Session):
    if is_unconcluded_event_today(session):
        calendar = get_calendar(session)
        calendar_event = calendar.get(sim_time)
        if calendar_event.league is not None:
            add_event_starting_news(
                calendar_event.league.name,
                sum(
                    1
                    for x in calendar.values()
                    if x.concluded and x.league is not None and x.league.level == calendar_event.league.level
                ) + 1,
                calendar_event.event_type,
                session
            )


def _hand_out_pensions(session: Session, sim_time: int):
    """ Apply pension payouts for retired blobs if pension policies active """

    pension_policy = get_active_policy_by_type(session, PolicyType.PENSION_SCHEME, sim_time)
    if pension_policy:
        retired = get_all_retired(session)
        base = 1
        chance = 0.1 * (pension_policy.applied_level - 1)
        if chance > 1:
            chance = 1
        for r in retired:
            r.money += base
            if random.random() < chance:
                r.money += 1
        # save retired blobs
        if retired:
            save_all_blobs(session, retired)
