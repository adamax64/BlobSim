import random
from data.db.db_engine import transactional
from data.persistence.action_repository import (
    get_action_by_event_and_blob,
    get_all_actions_by_event,
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
    Generate score for contender and save the action for given event.
    """
    score = contender.strength * random.random()
    is_new_record = is_quartered_score_new_record(session, score)
    action = get_action_by_event_and_blob(session, event_id, contender.id)
    action.scores = action.scores + [score]
    save_action(session, action)
    return is_new_record


@transactional
def create_actions_for_race(contenders: list[BlobCompetitorDto], event_id: int, tick: int, session) -> None:
    """
    Generate score for contender and save the action for given event.
    Save only if no actions exist for the same event and tick.
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
