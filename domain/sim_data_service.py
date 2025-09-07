import random
from data.db.db_engine import transactional
from data.model.calendar import Calendar
from data.persistence.sim_data_repository import get_sim_data, save_sim_data
from data.persistence.calendar_repository import get_calendar
from domain.calendar_service import recreate_calendar_for_next_season
from domain.league_service import manage_league_transfers
from domain.utils.constants import BLOB_CREATION_RESOURCES
from domain.utils.sim_time_utils import get_season, is_season_end


@transactional
def get_sim_time(session) -> int:
    return get_sim_data(session).sim_time


@transactional
def is_unconcluded_event_today(session) -> bool:
    time = get_sim_time()
    calendar = get_calendar(session)

    if time in calendar:
        return not calendar[time].concluded
    else:
        return False


@transactional
def reset_factory_progress(session):
    """Substract factory progress value by the resource amount sufficient for blob creation"""

    sim_data = get_sim_data(session)
    sim_data.factory_progress -= BLOB_CREATION_RESOURCES
    save_sim_data(session, sim_data)


@transactional
def get_current_calendar(session) -> Calendar | None:
    return get_calendar(session).get(get_sim_time(session))


@transactional
def is_current_event_concluded(session) -> bool:
    current_calendar = get_current_calendar(session)
    if current_calendar is None:
        return True
    return current_calendar.concluded


@transactional
def get_event_next_day(session) -> Calendar | None:
    return get_calendar(session).get(get_sim_time(session) + 1)


@transactional
def progress_simulation(session):
    sim_data = get_sim_data(session)
    if is_season_end(sim_data.sim_time):
        manage_league_transfers(session, get_season(sim_data.sim_time))
        recreate_calendar_for_next_season(session, get_season(sim_data.sim_time) + 1)

    sim_data.factory_progress += random.randint(1, 5)
    sim_data.sim_time += 1
    save_sim_data(session, sim_data)


@transactional
def is_blob_created(session) -> bool:
    return get_sim_data(session).factory_progress >= BLOB_CREATION_RESOURCES


@transactional
def get_factory_progress(session) -> int:
    return get_sim_data(session).factory_progress
