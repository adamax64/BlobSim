from domain.blob_services.blob_update_service import update_blob_speed_by_id
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_record_dto import RaceEventRecordDto
from domain.utils.constants import OVERTAKE_EFFECT


def get_race_event_records(actions: list[ActionDto], competitors: list[BlobCompetitorDto], is_playback: bool) -> list[RaceEventRecordDto]:
    event_records_by_competitors = {competitor.id: RaceEventRecordDto(blob=competitor, distance_records=[]) for competitor in competitors}

    current_tick = max((len(action.scores) for action in actions), default=0)

    for tick in range(current_tick):
        for action in actions:
            if len(action.scores) > tick:
                competitor = event_records_by_competitors[action.blob_id]
                previous_distance = competitor.distance_records[-1] if len(competitor.distance_records) > 0 else 0
                competitor.distance_records.append(previous_distance + action.scores[tick])
        if tick == current_tick - 2:
            sorted_competitors = sorted(event_records_by_competitors.values(), key=_race_sort_lambda(), reverse=True)
            for i, competitor in enumerate(sorted_competitors):
                competitor.previous_position = i + 1

    # If a competitor overtakes another, or is overtaken, they learn from it.
    current_sorted = sorted(event_records_by_competitors.values(), key=_race_sort_lambda(), reverse=True)
    if not is_playback and current_tick > 1:
        for i, competitor in enumerate(current_sorted):
            current_position = i + 1
            prev_position = competitor.previous_position
            overtakes = prev_position - current_position
            if overtakes > 0:
                update_blob_speed_by_id(competitor.blob.id, overtakes * OVERTAKE_EFFECT)
            elif overtakes < 0:
                update_blob_speed_by_id(competitor.blob.id, overtakes * OVERTAKE_EFFECT)

    return current_sorted


def _race_sort_lambda():
    return lambda x: x.distance_records[-1] if len(x.distance_records) > 0 else 0
