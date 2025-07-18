from collections import defaultdict
import random
from domain.blob_service import update_blob_speed_by_id
from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.event_record_dto import EventRecordDto, QuarteredEventRecordDto, RaceEventRecordDto, ScoreDto
from domain.utils.constants import OVERTAKE_EFFECT, OVERTAKEN_EFFECT


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
        return _get_quartered_event_records(actions, competitors, event_type)
    else:
        return _get_race_event_records(actions, competitors, is_playback)


def _get_quartered_event_records(
    actions: list[ActionDto],
    competitors: list[BlobCompetitorDto],
    event_type: EventTypeDto
) -> list[QuarteredEventRecordDto]:
    random.shuffle(competitors)
    quarter_ends = _get_quarter_ends(len(competitors), event_type)
    records = {blob.id: QuarteredEventRecordDto(blob, [ScoreDto(), ScoreDto(), ScoreDto(), ScoreDto()]) for blob in competitors}

    if len(actions) == 0:
        result_records = list(records.values())
        result_records[0].next = True
        return result_records

    quarter = 1
    for action in actions:
        quarter = _get_current_quarter(quarter_ends, action.tick)
        score = records[action.blob_id].quarters[quarter - 1]

        if action.tick == len(actions) - 1 and score.score is not None and score.score >= action.score:
            score.latest_score = action.score

        if score.score is None or score.score < action.score:
            score.score = action.score
            if action.tick == len(actions) - 1:
                score.personal_best = True

    if len(actions) > 0:
        current_quarter = _get_current_quarter(quarter_ends, len(actions))

        latest_action = actions[-1]
        current_record = records[latest_action.blob_id]
        current_record.current = True

    result_records = list(records.values())

    if len(actions) > 0:
        current_quarter = _get_current_quarter(quarter_ends, len(actions))

        for q in range(current_quarter - 1):
            result_records.sort(key=_quartered_sort_lambda(q), reverse=True)
            result_records[0].quarters[q].best = True
            for index, record in enumerate(result_records):
                record.eliminated = _is_eliminated(q + 1, len(competitors), index + 1)
        if current_quarter == quarter:
            result_records.sort(key=_quartered_sort_lambda(quarter - 1), reverse=True)

    next_index = _get_quarter_index(quarter_ends, len(actions), len(competitors))
    if len(result_records) > next_index >= 0:
        result_records[next_index].next = True

    return result_records


def _get_current_quarter(quarter_ends: list[int], tick: int) -> int:
    for i, end in enumerate(quarter_ends):
        if tick < end:
            return i + 1
    return 5


def _get_quarter_ends(field_size: int, event_type: EventTypeDto) -> list[int]:
    eliminations = _get_eliminations(field_size)
    multiplyer = 1
    if event_type == EventTypeDto.QUARTERED_TWO_SHOT_SCORING:
        multiplyer = 2
    return [
        multiplyer * (field_size),
        multiplyer * (2 * field_size - eliminations),
        multiplyer * (3 * field_size - 3 * eliminations),
        multiplyer * (4 * field_size - 6 * eliminations)
    ]


def _get_eliminations(field_size: int) -> int:
    return int((field_size - 3) / 3) if field_size < 15 else int(field_size / 4)


def _quartered_sort_lambda(index: int):
    return lambda x: (
                    x.quarters[index].score is not None,
                    x.quarters[index].score if x.quarters[index] is not None else -1
                )


def _is_eliminated(quarter: int, field_size: int, position: int) -> int:
    eliminations = quarter * _get_eliminations(field_size)
    threshold = field_size - eliminations
    return position > threshold


def _get_quarter_index(quarter_ends: list[int], tick: int, field_size: int) -> int:
    quarter = _get_current_quarter(quarter_ends, tick)
    if quarter == 1:
        return tick % field_size if field_size > 0 else 0
    else:
        current_field_size = field_size - (quarter - 1) * _get_eliminations(field_size)
        quarter_tick = tick - quarter_ends[quarter - 2]
        return quarter_tick % current_field_size if current_field_size > 0 else 0


def _get_race_event_records(actions: list[ActionDto], competitors: list[BlobCompetitorDto], is_playback: bool) -> list[RaceEventRecordDto]:
    actions_by_tick = defaultdict(list[ActionDto])
    for action in actions:
        if action.tick not in actions_by_tick:
            actions_by_tick[action.tick] = []
        actions_by_tick[action.tick].append(action)

    event_records_by_competitors = {competitor.id: RaceEventRecordDto(blob=competitor, distance_records=[]) for competitor in competitors}

    if len(actions) == 0:
        result_records = list(event_records_by_competitors.values())
        random.shuffle(result_records)
        return result_records

    previous_tick = sorted(actions_by_tick.keys(), reverse=True)[1] if len(actions_by_tick.keys()) > 1 else None
    for tick in actions_by_tick.keys():
        actions = actions_by_tick[tick]
        for action in actions:
            competitor = event_records_by_competitors[action.blob_id]
            previous_distance = competitor.distance_records[-1] if len(competitor.distance_records) > 0 else 0
            competitor.distance_records.append(previous_distance + action.score)
        if tick == previous_tick:
            sorted_competitors = sorted(event_records_by_competitors.values(), key=_race_sort_lambda(), reverse=True)
            for i, competitor in enumerate(sorted_competitors):
                competitor.previous_position = i + 1

    if previous_tick is None:
        for i, competitor in enumerate(event_records_by_competitors.values()):
            competitor.previous_position = i + 1

    # If a competitor overtakes another, or is overtaken, they learn from it.
    current_sorted = sorted(event_records_by_competitors.values(), key=_race_sort_lambda(), reverse=True)
    if not is_playback and previous_tick is not None:
        for i, competitor in enumerate(current_sorted):
            current_position = i + 1
            prev_position = competitor.previous_position
            overtakes = prev_position - current_position
            if overtakes > 0:
                update_blob_speed_by_id(competitor.blob.id, overtakes * OVERTAKE_EFFECT)
            elif overtakes < 0:
                update_blob_speed_by_id(competitor.blob.id, overtakes * OVERTAKEN_EFFECT)

    return current_sorted


def _race_sort_lambda():
    return lambda x: x.distance_records[-1] if len(x.distance_records) > 0 else 0
