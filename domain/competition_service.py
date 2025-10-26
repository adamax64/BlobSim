from data.db.db_engine import transactional
from data.model.result import Result
from data.persistence.blob_reposiotry import save_all_blobs
from data.persistence.result_repository import save_all_results
from domain.calendar_service import conclude_calendar_event
from domain.dtos.event_dto import EventDto
from domain.dtos.event_record_dto import EliminationEventRecordDto, EventRecordDto, QuarteredEventRecordDto
from domain.event_service import get_or_start_event
from domain.exceptions.no_current_event_exception import NoCurrentEventException
from domain.news_services.news_service import add_event_ended_news
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
def process_event_results(event: EventDto, event_records: list[EventRecordDto], session):
    """
    Calculates the points for the contenders by position and event type, and saves them in result objects to the database.
    This function also administrates the trophies and medals, gives out the victory prize and saves a news entry about the event results.
    """

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
    sorted_results: list[Result] = sorted(saved_results, key=lambda x: x.position)
    add_event_ended_news(
        event.league.name,
        event.round,
        sorted_results[0].blob.id,
        sorted_results[1].blob.id,
        sorted_results[2].blob.id,
        session
    )


def _map_records_to_results(event_records: list[EventRecordDto], event_id: int) -> list[Result]:
    results = []

    # For elimination events, find the blob with most wins
    max_wins = _get_max_tick_wins(event_records)

    for i, record in enumerate(event_records):
        bonus_points = _calculate_bonus_points(record, i + 1, max_wins)

        # Add bonus point for most wins in elimination events
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


def _calculate_bonus_points(record: EventRecordDto, position: int, max_wins: int | None) -> int:
    if isinstance(record, QuarteredEventRecordDto):
        return sum(1 for quarter in record.quarters if quarter.best is True)
    elif isinstance(record, EliminationEventRecordDto):
        bonus_points = 0
        if record.tick_wins > 0:
            bonus_points += 1
        if record.tick_wins == max_wins:
            bonus_points += 1
        if position == 1:
            bonus_points += 1
        return bonus_points
    else:
        return 1 if position == 1 else 0


def _get_max_tick_wins(event_records: list[EventRecordDto]) -> int | None:
    """Get the maximum tick wins for elimination events. Returns None for non-elimination events."""
    if not event_records or not isinstance(event_records[0], EliminationEventRecordDto):
        return None
    max_value = max((record.tick_wins for record in event_records), default=0)
    occurrence_count = sum(1 for record in event_records if record.tick_wins == max_value)
    return max_value if occurrence_count == 1 else None
