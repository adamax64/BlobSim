import random
from data.db.db_engine import transactional
from data.model.action import Action
from data.persistence.action_repository import (
    is_quartered_score_new_record,
    save_action, save_all_actions,
    actions_exist_for_event_and_tick
)
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.sim_data_service import get_sim_time
from domain.utils.action_utils import generate_race_score_for_contender
from domain.utils.league_utils import get_race_duration_by_size


@transactional
def create_action_for_quartered_event(contender: BlobCompetitorDto, event_id: int, tick: int, session) -> bool:
    """
    Generate score for contender and save the action for given event.
    """
    score = contender.strength * random.random()
    is_new_record = is_quartered_score_new_record(session, contender.id, score)
    save_action(session, Action(
        event_id=event_id,
        tick=tick,
        blob_id=contender.id,
        score=score
    ))
    return is_new_record


@transactional
def create_actions_for_race(contenders: list[BlobCompetitorDto], event_id: int, tick: int, session) -> None:
    """
    Generate score for contender and save the action for given event.
    Save only if no actions exist for the same event and tick.
    """
    if actions_exist_for_event_and_tick(session, event_id, tick):
        raise Exception("Actions already exist for this event and tick")

    current_time = get_sim_time(session)
    race_duration = get_race_duration_by_size(len(contenders))
    actions = []
    for contender in contenders:
        score = generate_race_score_for_contender(contender, current_time, race_duration, tick)
        actions.append(
            Action(
                event_id=event_id,
                tick=tick,
                blob_id=contender.id,
                score=score
            )
        )
    save_all_actions(session, actions)
    return score
