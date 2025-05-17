from data.db.db_engine import transactional
from data.model.result import Result
from data.persistence.blob_reposiotry import save_all_blobs
from data.persistence.result_repository import save_all_results
from domain.calendar_service import conclude_calendar_event
from domain.dtos.event_dto import EventDto
from domain.dtos.event_record_dto import EventRecordDto, QuarteredEventRecordDto
from domain.event_service import get_or_start_event
from domain.exceptions.no_current_event_exception import NoCurrentEventException
from domain.sim_data_service import get_current_calendar
from domain.utils.constants import VICTORY_PRIZE


@transactional
def load_competition_data(session) -> EventDto:
    """ Load the current event data from the database. If no event is found, start a new one. """
    league_id = get_current_calendar(session).league_id
    if league_id is None:
        raise NoCurrentEventException()
    return get_or_start_event(session, league_id, False)


@transactional
def save_event_results(event: EventDto, event_records: list[EventRecordDto], session):
    results = _map_records_to_results(event_records, event.id)
    saved_results = save_all_results(session, results)

    for result in saved_results:
        if result.position == 1:
            if event.league.level == 1:
                result.blob.gold_trophies += 1
            else:
                result.blob.gold_medals += 1
            result.blob.money += VICTORY_PRIZE
        if result.position == 2:
            if event.league.level == 1:
                result.blob.silver_trophies += 1
            else:
                result.blob.silver_medals += 1
        if result.position == 3:
            if event.league.level == 1:
                result.blob.bronze_trophies += 1
            else:
                result.blob.bronze_medals += 1

        result.blob.points += result.points
    save_all_blobs(session, [res.blob for res in saved_results])

    conclude_calendar_event(session)


def _map_records_to_results(event_records: list[EventRecordDto], event_id: int) -> list[Result]:
    results = []
    for i, record in enumerate(event_records):
        bonus_points = _calculate_bonus_points(record, i + 1)
        results.append(Result(
            event_id=event_id,
            blob_id=record.blob.id,
            position=i + 1,
            points=_calculate_points(i + 1, len(event_records), bonus_points)
        ))
    return results


def _calculate_points(position: int, field_size: int, bonus_points: int) -> int:
    base = field_size - position + 1
    if position in (1, 2, 3) and field_size >= 7:
        base += (4 - position)
    if field_size < 7 and position == 1:
        base += 1
    return base + bonus_points


def _calculate_bonus_points(record: EventRecordDto, position: int) -> int:
    if isinstance(record, QuarteredEventRecordDto):
        return sum(1 for quarter in record.quarters if quarter.best is True)
    else:
        return 1 if position == 1 else 0
