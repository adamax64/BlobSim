from domain.dtos.action_dto import ActionDto
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.dtos.event_record_dto import EliminationEventRecordDto


def get_elimination_event_records(
    actions: list[ActionDto],
    competitors: list[BlobCompetitorDto]
) -> list[EliminationEventRecordDto]:
    competitors_by_id = {competitor.id: competitor for competitor in competitors}
    current_tick = max((len(action.scores) for action in actions), default=0)

    if current_tick == 0:
        return [EliminationEventRecordDto(blob=competitor, last_score=None, eliminated=False) for competitor in competitors]

    elimination_records = []
    sorted_actions = sorted(actions, key=(lambda a: (len(a.scores), a.scores[-1])), reverse=True)
    for action in sorted_actions:
        elimination_records.append(EliminationEventRecordDto(
            blob=competitors_by_id.get(action.blob_id),
            last_score=action.scores[-1],
            eliminated=len(action.scores) < current_tick
        ))

    elimination_records[-current_tick].eliminated = True

    return elimination_records
