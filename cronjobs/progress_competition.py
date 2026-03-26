from types import TracebackType

from data.db.db_engine import transactional
from data.model.event_type import EventType
from domain.competition_service import load_competition_data, process_event_results
from domain.action_service import (
    create_actions_for_race,
    create_action_for_quartered_event,
    create_actions_for_elimination_event,
)
from domain.dtos.event_dto import EventDto
from domain.event_record_services.quartered_event_record_service import get_quarter_ends
from domain.sim_data_service import is_unconcluded_event_today
from domain.event_record_services.event_record_service import get_event_records
from domain.calendar_service import conclude_calendar_event
from domain.dtos.event_record_dto import (
    EliminationEventRecordDto,
    QuarteredEventRecordDto,
    SprintEventRecordDto,
)
from data.persistence.action_repository import get_all_actions_by_event
from domain.utils.league_utils import get_race_duration_by_size


def should_conclude_event(event: EventDto, event_records, session) -> bool:
    """
    Determine if an event should be concluded based on event type and records.
    - Sprint races: conclude when all competitors are finished or max tick reached
    - Endurance races: conclude after a max number of ticks
    - Elimination: conclude when only one competitor remains
    - Quartered scoring: conclude after all quarters are completed
    """
    if event.type == EventType.SPRINT_RACE:
        current_tick = max(
            (len(record.distance_records) for record in event_records), default=0
        )
        max_tick = get_race_duration_by_size(len(event.competitors))
        # Conclude if all competitors have finished or max tick reached
        if current_tick >= max_tick:
            return True

        return all(
            isinstance(record, SprintEventRecordDto) and record.is_finished
            for record in event_records
        )
    elif event.type == EventType.ENDURANCE_RACE:
        # Conclude after max ticks
        max_ticks = get_race_duration_by_size(len(event.competitors))
        return (
            len(event_records[0].distance_records) >= max_ticks
            if event_records
            else False
        )
    elif event.type == EventType.ELIMINATION_SCORING:
        # Conclude when only one competitor is not eliminated
        remaining = sum(
            1
            for record in event_records
            if isinstance(record, EliminationEventRecordDto) and not record.eliminated
        )
        return remaining <= 1
    elif event.type in [
        EventType.QUARTERED_ONE_SHOT_SCORING,
        EventType.QUARTERED_TWO_SHOT_SCORING,
    ]:
        quarter_ends = get_quarter_ends(len(event.competitors), event.type)
        current_tick = (
            sum(
                len(action.scores)
                for action in get_all_actions_by_event(session, event.id)
            )
            if event_records
            else 0
        )
        return current_tick >= quarter_ends[-1]  # Conclude after last quarter ends
    return False


@transactional
def progress_competition(session):
    try:
        if not is_unconcluded_event_today(session):
            return

        event = load_competition_data(session)
        if event.type in [EventType.SPRINT_RACE, EventType.ENDURANCE_RACE]:
            # Get current max tick
            actions = get_all_actions_by_event(session, event.id)
            current_max_tick = max(
                (len(action.scores) for action in actions), default=0
            )
            tick = current_max_tick
            create_actions_for_race(event.competitors, event.id, tick, session)
            print(f"[INFO] Progressed competition for event {event.id}, tick {tick}")

        elif event.type in [
            EventType.QUARTERED_ONE_SHOT_SCORING,
            EventType.QUARTERED_TWO_SHOT_SCORING,
        ]:
            # Get event records to determine which competitors are still active
            event_records = get_event_records(
                event.actions, event.competitors, event.type, is_playback=False
            )

            next_blob = next(
                (
                    record.blob
                    for record in event_records
                    if isinstance(record, QuarteredEventRecordDto) and record.next
                ),
                None,
            )

            if next_blob:
                create_action_for_quartered_event(next_blob, event.id, session)
                print(
                    f"[INFO] Progressed competition for event {event.id}, quartered event"
                )
            else:
                print(f"[WARNING] No active competitors for event {event.id}")

        elif event.type == EventType.ELIMINATION_SCORING:
            # Get event records to determine which competitors are still active
            event_records = get_event_records(
                event.actions, event.competitors, event.type, is_playback=False
            )

            # Filter active (non-eliminated) competitors
            active_competitors = [
                record.blob
                for record in event_records
                if isinstance(record, EliminationEventRecordDto)
                and not record.eliminated
            ]

            if active_competitors:
                create_actions_for_elimination_event(
                    active_competitors, event.id, session
                )
                print(
                    f"[INFO] Progressed competition for event {event.id}, elimination event"
                )
            else:
                print(f"[INFO] No active competitors for event {event.id}")
        else:
            print("[INFO] Event type not supported for progression yet")

        # Check if event should be concluded
        event_records = get_event_records(
            get_all_actions_by_event(session, event.id),
            event.competitors,
            event.type,
            is_playback=False,
        )

        if should_conclude_event(event, event_records, session):
            process_event_results(event, event_records, session)
            conclude_calendar_event(session)
            print(f"[INFO] Concluded event {event.id}")

    except Exception as e:
        print(f"[ERROR] Error progressing competition: {e.with_traceback(None)}")
