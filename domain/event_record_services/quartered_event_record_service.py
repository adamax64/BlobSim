from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.event_record_dto import QuarteredEventRecordDto, ScoreDto


def get_quartered_event_records(
    actions: list[ActionDto],
    competitors: list[BlobCompetitorDto],
    event_type: EventTypeDto
) -> list[QuarteredEventRecordDto]:
    quarter_ends = _get_quarter_ends(len(competitors), event_type)

    # Create a mapping from blob_id to BlobCompetitorDto for quick lookup
    blob_map = {blob.id: blob for blob in competitors}
    records = [
        QuarteredEventRecordDto(
            blob=blob_map.get(blob_id),
            quarters=[ScoreDto(), ScoreDto(), ScoreDto(), ScoreDto()]
        )
        for blob_id in blob_map.keys()
    ]
    actions_by_blob_id = {action.blob_id: action for action in actions}

    current_tick = sum(len(action.scores) for action in actions)

    quarter = 1
    for tick in range(current_tick + 1):
        quarter = _get_current_quarter(quarter_ends, tick)
        if quarter == 5:
            continue

        quarter_tick = tick if quarter == 1 else tick - quarter_ends[quarter - 2]
        record = _get_current_record(
            records,
            quarter_tick,
            quarter_ends[0] if quarter == 1 else quarter_ends[quarter - 1] - quarter_ends[quarter - 2],
            event_type
        )
        # If the tick is the current tick, set the record to current
        if tick == current_tick:
            record.next = True
            for i, record in enumerate(records):
                record.eliminated = _is_eliminated(quarter - 1, len(competitors), i + 1)
            continue

        score = record.quarters[quarter - 1]
        action_score = _get_current_score(actions_by_blob_id.get(record.blob.id), quarter_tick, quarter, event_type, len(competitors))
        if score.score is None or score.score < action_score:
            score.score = action_score
            if tick == current_tick - 1:
                score.personal_best = True
        elif score.score >= action_score and tick == current_tick - 1:
            score.latest_score = action_score
        records.sort(key=_quartered_sort_lambda(quarter - 1), reverse=True)

        if tick + 1 in quarter_ends:
            records[0].quarters[quarter - 1].best = True

        if tick == current_tick - 1:
            record.current = True

    return records


def _get_current_score(action: ActionDto, tick: int, quarter: int, event_type: EventTypeDto, field_size: int) -> float:
    eliminations = _get_eliminations(field_size)
    quarter_index = quarter - 1
    if event_type == EventTypeDto.QUARTERED_TWO_SHOT_SCORING:
        return action.scores[(quarter_index) * 2 + (1 if tick >= field_size - (eliminations * (quarter_index)) else 0)]
    else:
        return action.scores[quarter_index]


def _get_current_record(
    records: list[QuarteredEventRecordDto],
    tick: int,
    quarter_length: int,
    event_type: EventTypeDto
) -> QuarteredEventRecordDto:
    if event_type == EventTypeDto.QUARTERED_TWO_SHOT_SCORING:
        return records[int(tick - quarter_length / 2) if tick >= quarter_length / 2 else tick]
    else:
        return records[tick]


def _get_current_quarter(quarter_ends: list[int], tick: int) -> int:
    ''' Returns the current quarter based on the tick. (1-4)'''
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


def _is_eliminated(quarter: int, field_size: int, position: int) -> bool:
    eliminations = quarter * _get_eliminations(field_size)
    threshold = field_size - eliminations
    return position > threshold
