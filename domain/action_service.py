import random
from data.db.db_engine import transactional
from data.persistence.action_repository import (
    get_action_by_event_and_blob,
    get_all_actions_by_event,
    is_elimination_score_new_record,
    is_quartered_score_new_record,
    save_action, save_all_actions,
)
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.sim_data_service import get_sim_time
from domain.utils.action_utils import generate_race_score_for_contender
from domain.utils.league_utils import get_race_duration_by_size


@transactional
def create_action_for_quartered_event(contender: BlobCompetitorDto, event_id: int, session) -> bool:
    """
    Generate score and update the action for given event and blob.
    Score is based on strength (70%) and speed (30%) attributes.
    """
    score = contender.strength * random.random() * 0.7 + contender.speed * random.random() * 0.3
    is_new_record = is_quartered_score_new_record(session, score)
    action = get_action_by_event_and_blob(session, event_id, contender.id)
    action.scores = action.scores + [score]
    save_action(session, action)
    return is_new_record


@transactional
def create_actions_for_race(contenders: list[BlobCompetitorDto], event_id: int, tick: int, session) -> None:
    """
    Generate score and update the actions for given event and the corresponding contenders.
    """
    actions = get_all_actions_by_event(session, event_id)
    actions = {action.blob_id: action for action in actions}

    if max((len(action.scores) for action in actions.values()), default=0) > tick:
        raise Exception("Actions already exist for this event and tick")

    current_time = get_sim_time(session)
    race_duration = get_race_duration_by_size(len(contenders))
    for contender in contenders:
        score = generate_race_score_for_contender(contender, current_time, race_duration, tick)
        actions[contender.id].scores = actions[contender.id].scores + [score]
    save_all_actions(session, actions.values())
    return score


@transactional
def create_actions_for_elimination_event(contenders: list[BlobCompetitorDto], event_id: int, session) -> tuple[str, float] | None:
    """ Generate score by contender strngth and update the actions for elimination event. """

    actions = get_all_actions_by_event(session, event_id)
    actions = {action.blob_id: action for action in actions}
    max_score = 0
    max_scorer_name = None
    for contender in contenders:
        score = contender.strength * random.random()
        actions[contender.id].scores = actions[contender.id].scores + [score]
        if score > max_score:
            max_score = score
            max_scorer_name = contender.name
    save_all_actions(session, actions.values())

    if is_elimination_score_new_record(session, max_score):
        return max_scorer_name, max_score
    return None
