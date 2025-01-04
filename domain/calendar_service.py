from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.calendar import Calendar
from data.model.event_type import EventType
from data.persistence.calendar_repository import (
    clear_calendar, get_calendar, get_next_unconcluded,
    save_all_calendar_records, save_calendar_event
)
from data.persistence.league_repository import get_all_real_leagues
from domain.dtos.calendar_dto import CalendarDto
from domain.utils.event_utils import pick_random_event_type
from domain.utils.league_utils import (
    HALF_SEASON, INACTIVE_SEASON, LONG_SEASON, MAXIMAL_SEASON, MEDIUM_SEASON,
    MINIMAL_SEASON, SHORT_SEASON, get_epoch_cycle_by_level, get_number_of_rounds_by_size
)
from domain.utils.sim_time_utils import get_sim_time_from


@transactional
def conclude_calendar_event(session: Session):
    calendar = get_next_unconcluded(session)
    if calendar.concluded:
        raise Exception('Calendar event already concluded')
    calendar.concluded = True
    save_calendar_event(session, calendar)


@transactional
def get_season_calendar(session: Session) -> CalendarDto:
    calendar = get_calendar(session).values()
    return [CalendarDto(event.date, event.league.name, event.concluded) for event in calendar]


@transactional
def recreate_calendar_for_next_season(session: Session, next_season: int):
    clear_calendar(session)
    leagues = get_all_real_leagues(session)
    calendar = []
    for league in leagues:
        cycle = get_epoch_cycle_by_level(league.level)
        field_size = len(league.players)
        rounds = get_number_of_rounds_by_size(field_size)
        if rounds == INACTIVE_SEASON:
            continue
        if rounds == MINIMAL_SEASON:     # epochs 6, 13, 21, 28
            calendar.append(_create_calendar_record(next_season, 6, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 13, cycle, league.id, EventType.QUARTERED_ONE_SHOT_SCORING))
            calendar.append(_create_calendar_record(next_season, 21, cycle, league.id, EventType.QUARTERED_TWO_SHOT_SCORING))
            calendar.append(_create_calendar_record(next_season, 28, cycle, league.id))
        if rounds == SHORT_SEASON:      # epochs 3, 10, 18, 25
            calendar.append(_create_calendar_record(next_season, 3, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 10, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 18, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 25, cycle, league.id))
        if rounds == HALF_SEASON:       # epochs 8, 15, 23, 30
            calendar.append(_create_calendar_record(next_season, 8, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 15, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 23, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 30, cycle, league.id))
        if rounds == MEDIUM_SEASON:     # epochs 5, 12, 20, 27
            calendar.append(_create_calendar_record(next_season, 5, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 12, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 20, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 27, cycle, league.id))
        if rounds == LONG_SEASON:       # epochs 7, 14, 22, 29
            calendar.append(_create_calendar_record(next_season, 7, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 14, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 22, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 29, cycle, league.id))
        if rounds == MAXIMAL_SEASON:    # epochs 4, 11, 19, 26
            calendar.append(_create_calendar_record(next_season, 4, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 11, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 19, cycle, league.id))
            calendar.append(_create_calendar_record(next_season, 26, cycle, league.id))

    calendar.sort(key=lambda x: x.date)
    save_all_calendar_records(session, calendar)


def _create_calendar_record(season, epoch, cycle, league_id, event_type=pick_random_event_type()):
    return Calendar(
        date=get_sim_time_from(season, epoch, cycle),
        league_id=league_id,
        concluded=False,
        event_type=event_type
    )
