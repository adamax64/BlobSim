import random
from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.persistence.calendar_repository import get_calendar
from data.persistence.sim_data_repository import get_sim_data, save_sim_data
from domain.blob_services.blob_creation_service import check_factory_and_create_blob
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

    sim_data.factory_progress += random.randint(1, 5)
    sim_data.sim_time += 1
    save_sim_data(session, sim_data)

    _check_and_add_event_news(sim_data.sim_time, session)
    check_factory_and_create_blob(session)


def _inagruate_grandmaster(current_season: int, session: Session):
    standings = get_grandmaster_standings(current_season - 3, current_season, session)
    grandmaster = standings[0]
    add_new_grandmaster_news(grandmaster.name, session)


def _check_and_add_event_news(sim_time: int, session: Session):
    if is_unconcluded_event_today(session):
        calendar = get_calendar(session)
        calendar_event = calendar.get(sim_time)
        add_event_starting_news(
            calendar_event.league.name,
            sum(
                1
                for x in calendar.values()
                if not x.concluded and x.league.level == calendar_event.league.level
            ),
            calendar_event.event_type,
            session
        )
