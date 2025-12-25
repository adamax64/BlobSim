from domain.blob_services.blob_update_service import update_blob_speed_by_id
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_record_dto import RaceEventRecordDto, SprintEventRecordDto
from domain.utils.constants import OVERTAKE_EFFECT
from domain.utils.league_utils import get_race_duration_by_size


def get_endurance_event_records(
        actions: list[ActionDto],
        competitors: list[BlobCompetitorDto],
        is_playback: bool
        ) -> list[RaceEventRecordDto]:
    event_records_by_competitors = {competitor.id: RaceEventRecordDto(blob=competitor, distance_records=[]) for competitor in competitors}

    current_tick = max((len(action.scores) for action in actions), default=0)

    for tick in range(current_tick):
        for action in actions:
            if len(action.scores) > tick:
                competitor = event_records_by_competitors[action.blob_id]
                previous_distance = competitor.distance_records[-1] if len(competitor.distance_records) > 0 else 0
                competitor.distance_records.append(previous_distance + action.scores[tick])
        if tick == current_tick - 2:
            sorted_competitors = sorted(event_records_by_competitors.values(), key=_endurance_sort_lambda(), reverse=True)
            for i, competitor in enumerate(sorted_competitors):
                competitor.previous_position = i + 1

    # If a competitor overtakes another, or is overtaken, they learn from it.
    current_sorted = sorted(event_records_by_competitors.values(), key=_endurance_sort_lambda(), reverse=True)
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


def get_sprint_event_records(
        actions: list[ActionDto],
        competitors: list[BlobCompetitorDto],
        is_playback: bool
        ) -> list[SprintEventRecordDto]:
    """Sprint race ordering: competitors finish when their cumulative distance reaches race length.

    The race length equals the number of distance units given by get_race_duration_by_size(field_size).
    If multiple blobs finish in the same tick, the tie-breaker is the time within that tick they reached the finish:
    (length_left_before_tick) / (score_in_finish_tick). Smaller is earlier.
    """
    event_records_by_competitors = {competitor.id: SprintEventRecordDto(blob=competitor, distance_records=[]) for competitor in competitors}

    current_tick = max((len(action.scores) for action in actions), default=0)
    race_length = get_race_duration_by_size(len(competitors))

    # Build cumulative distances per tick
    for tick in range(current_tick):
        for action in actions:
            if len(action.scores) > tick:
                competitor = event_records_by_competitors[action.blob_id]
                previous_distance = competitor.distance_records[-1] if len(competitor.distance_records) > 0 else 0
                # append cumulative distance
                competitor.distance_records.append(previous_distance + action.scores[tick])
                # mark as finished if reaching race length in this tick and compute fractional time within the tick
                if not competitor.is_finished and competitor.distance_records[-1] >= race_length:
                    score = action.scores[tick]
                    remaining = race_length - previous_distance
                    if score > 0:
                        # store absolute finish time: tick + fractional part within the tick
                        competitor.time = float(tick) + float(remaining) / score
                    else:
                        # should not happen, but safeguard against division by zero
                        competitor.time = float('inf')
                    competitor.is_finished = True
        # store previous_position near the end similar to endurance logic
        if tick == current_tick - 2:
            sorted_competitors = sorted(event_records_by_competitors.values(), key=_sprint_sort_lambda(), reverse=False)
            for i, competitor in enumerate(sorted_competitors):
                competitor.previous_position = i + 1

    # Determine final ordering
    current_sorted = sorted(event_records_by_competitors.values(), key=_sprint_sort_lambda(), reverse=False)

    # If a competitor overtakes another, or is overtaken, they learn from it. Keep existing behavior by comparing
    # previous_position and current ordering. Note that previous_position was stored relative to the sprint ordering above.
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


def _sprint_sort_lambda():
    """Return a key function that sorts competitors by sprint finish rules.

    With the SprintEventRecordDto properties available we can simplify the key:
      - finished flag (0 finished, 1 not finished)
      - finish time (fractional time smaller is earlier)
    For non-finishers we use -distance so blobs further along sort earlier.
    """
    def key(x: SprintEventRecordDto):
        if x.is_finished:
            return (0, x.time if x.time is not None else float('inf'))
        else:
            # non-finishers sort by negative distance at end of actions
            last_distance = x.distance_records[-1] if len(x.distance_records) > 0 else 0
            return (1, -last_distance)

    return key


def _endurance_sort_lambda():
    return lambda x: x.distance_records[-1] if len(x.distance_records) > 0 else 0
