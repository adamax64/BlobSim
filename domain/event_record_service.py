from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_dto import EventTypeDto
from domain.dtos.event_record_dto import EventRecordDto, QuarteredEventRecordDto, ScoreDto


def get_event_records(actions: ActionDto, competitors: BlobCompetitorDto, event_type: EventTypeDto) -> list[EventRecordDto]:
    if event_type == EventTypeDto.QUARTERED_TWO_SHOT_SCORING or event_type == EventTypeDto.QUARTERED_ONE_SHOT_SCORING:
        return get_quartered_event_records(actions, competitors, event_type)
    else:
        return []  # TODO: Implement other event types


def get_quartered_event_records(
    actions: ActionDto,
    competitors: BlobCompetitorDto,
    event_type: EventTypeDto
) -> list[QuarteredEventRecordDto]:
    quarter_ends = _get_quarter_ends(len(competitors), event_type)
    records = {blob.id: QuarteredEventRecordDto(blob, [ScoreDto(), ScoreDto(), ScoreDto(), ScoreDto()]) for blob in competitors}

    quarter = 1
    for action in actions:
        quarter = _get_current_quarter(quarter_ends, action.tick)
        print(quarter)
        score = records[action.blob_id].quarters[quarter - 1]
        if score.score is None or score.score < action.score:
            score.score = action.score

    result_records = list(records.values())

    if len(actions) > 0:
        current_quarter = _get_current_quarter(quarter_ends, len(actions))
        for q in range(current_quarter - 1):
            result_records.sort(key=_sort_lambda(q), reverse=True)
            result_records[0].quarters[q].best = True
        if current_quarter == quarter:
            result_records.sort(key=_sort_lambda(quarter - 1), reverse=True)

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
    return int((field_size - 3) / 3) if field_size < 15 else field_size / 4


def _sort_lambda(index: int):
    return lambda x: (
                    x.quarters[index].score is not None,
                    x.quarters[index].score if x.quarters[index] is not None else -1
                )
