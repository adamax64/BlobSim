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
        return [EliminationEventRecordDto(blob=competitor, last_score=None, eliminated=False, tick_wins=0) for competitor in competitors]

    # Calculate tick wins for each blob
    tick_wins_by_blob = {}
    for tick in range(current_tick):
        tick_scores = []
        for action in actions:
            if len(action.scores) > tick:
                tick_scores.append((action.blob_id, action.scores[tick]))
        if tick_scores:
            # Find the winner of this tick (highest score)
            winner_blob_id = max(tick_scores, key=lambda x: x[1])[0]
            tick_wins_by_blob[winner_blob_id] = tick_wins_by_blob.get(winner_blob_id, 0) + 1

    elimination_records = []
    sorted_actions = sorted(actions, key=(lambda a: (len(a.scores), a.scores[-1])), reverse=True)
    for action in sorted_actions:
        elimination_records.append(EliminationEventRecordDto(
            blob=competitors_by_id.get(action.blob_id),
            last_score=None if len(action.scores) < current_tick else action.scores[-1],
            eliminated=len(action.scores) < current_tick,
            tick_wins=tick_wins_by_blob.get(action.blob_id, 0)
        ))

    elimination_records[-current_tick].eliminated = True

    return elimination_records
