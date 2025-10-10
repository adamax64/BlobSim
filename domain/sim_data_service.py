from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.calendar import Calendar
from data.model.event_type import EventType
from data.persistence.sim_data_repository import get_sim_data, save_sim_data
from data.persistence.calendar_repository import get_calendar
from domain.utils.constants import BLOB_CREATION_RESOURCES
from domain.calendar_service import conclude_calendar_event


@transactional
def get_sim_time(session: Session) -> int:
    return get_sim_data(session).sim_time


@transactional
def is_unconcluded_event_today(session: Session) -> bool:
    time = get_sim_time()
    calendar = get_calendar(session)

    if time in calendar:
        # Automatically conclude catch-up training events
        if calendar[time].event_type == EventType.CATCHUP_TRAINING and not calendar[time].concluded:
            conclude_calendar_event(session)
            return False

        return not calendar[time].concluded
    else:
        return False


@transactional
def reset_factory_progress(session: Session):
    """ Substract factory progress value by the resource amount sufficient for blob creation """

    sim_data = get_sim_data(session)
    sim_data.factory_progress -= BLOB_CREATION_RESOURCES
    save_sim_data(session, sim_data)


@transactional
def get_current_calendar(session: Session) -> Calendar | None:
    return get_calendar(session).get(get_sim_time(session))


@transactional
def is_current_event_concluded(session: Session) -> bool:
    current_calendar = get_current_calendar(session)
    if current_calendar is None:
        return True
    return current_calendar.concluded


@transactional
def get_event_next_day(session: Session) -> Calendar | None:
    return get_calendar(session).get(get_sim_time(session) + 1)


@transactional
def is_blob_created(session: Session) -> bool:
    return get_sim_data(session).factory_progress >= BLOB_CREATION_RESOURCES


@transactional
def get_factory_progress(session: Session) -> int:
    return get_sim_data(session).factory_progress
