from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.event_record_dto import EventRecordDto
from domain.event_record_services.elimination_event_record_service import get_elimination_event_records
from domain.event_record_services.quartered_event_record_service import get_quartered_event_records
from domain.event_record_services.race_event_records_service import get_endurance_event_records, get_sprint_event_records


def get_event_records(
    actions: list[ActionDto],
    competitors: list[BlobCompetitorDto],
    event_type: EventTypeDto,
    is_playback: bool
) -> list[EventRecordDto]:
    if (
        event_type == EventTypeDto.QUARTERED_TWO_SHOT_SCORING
        or event_type == EventTypeDto.QUARTERED_ONE_SHOT_SCORING
    ):
        return get_quartered_event_records(actions, competitors, event_type)
    elif event_type == EventTypeDto.ENDURANCE_RACE:
        return get_endurance_event_records(actions, competitors, is_playback)
    elif event_type == EventTypeDto.SPRINT_RACE:
        return get_sprint_event_records(actions, competitors, is_playback)
    else:
        return get_elimination_event_records(actions, competitors)
