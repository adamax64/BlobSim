import random
from data.db.db_engine import transactional
from data.persistence.action_repository import (
    get_action_by_event_and_blob,
    get_all_actions_by_event,
    save_action, save_all_actions,
)
from data.persistence.event_repository import get_event_by_id
from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.record_service import check_and_update_record
from domain.sim_data_service import get_sim_time
from domain.utils.action_utils import generate_race_score_for_contender
from domain.utils.league_utils import get_race_duration_by_size


@transactional
def create_action_for_quartered_event(contender: BlobCompetitorDto, event_id: int, session) -> tuple[str, float] | None:
    """
    Generate score and update the action for given event and blob.
    Score is based on strength (70%) and speed (30%) attributes.
    Returns tuple of (name, score) if new record, None otherwise.
    """
    score = contender.strength * random.random() * 0.7 + contender.speed * random.random() * 0.3

    record = None
    # Get event information to check for records
    event = get_event_by_id(session, event_id)
    if event:
        is_new_record = check_and_update_record(event.league_id, event.type, contender.id, score, session)
        if is_new_record:
            record = (contender.name, score)

    action = get_action_by_event_and_blob(session, event_id, contender.id)
    action.scores = action.scores + [score]
    save_action(session, action)
    return record


@transactional
def create_actions_for_race(contenders: list[BlobCompetitorDto], event_id: int, tick: int, session) -> tuple[str, float] | None:
    """
    Generate score and update the actions for given event and the corresponding contenders.
    Returns tuple of (name, score) if new record, None otherwise.
    """
    actions = get_all_actions_by_event(session, event_id)
    actions = {action.blob_id: action for action in actions}

    if max((len(action.scores) for action in actions.values()), default=0) > tick:
        raise Exception("Actions already exist for this event and tick")

    current_time = get_sim_time(session)
    race_duration = get_race_duration_by_size(len(contenders))
    max_score = 0
    max_scorer_name = None
    max_scorer_id = None

    for contender in contenders:
        score = generate_race_score_for_contender(contender, current_time, race_duration, tick)
        actions[contender.id].scores = actions[contender.id].scores + [score]
        if score > max_score:
            max_score = score
            max_scorer_name = contender.name
            max_scorer_id = contender.id

    save_all_actions(session, actions.values())

    # Get event information to check for records
    event = get_event_by_id(session, event_id)
    if event and max_scorer_id:
        is_new_record = check_and_update_record(event.league_id, event.type, max_scorer_id, max_score, session)
        if is_new_record:
            return max_scorer_name, max_score
    return None


@transactional
def create_actions_for_elimination_event(contenders: list[BlobCompetitorDto], event_id: int, session) -> tuple[str, float] | None:
    """ Generate score by contender strngth and update the actions for elimination event. """

    actions = get_all_actions_by_event(session, event_id)
    actions = {action.blob_id: action for action in actions}
    max_score = 0
    max_scorer_name = None
    max_scorer_id = None

    for contender in contenders:
        score = contender.strength * random.random()
        actions[contender.id].scores = actions[contender.id].scores + [score]
        if score > max_score:
            max_score = score
            max_scorer_name = contender.name
            max_scorer_id = contender.id
    save_all_actions(session, actions.values())

    # Get event information to check for records
    event = get_event_by_id(session, event_id)
    if event and max_scorer_id:
        is_new_record = check_and_update_record(event.league_id, event.type, max_scorer_id, max_score, session)
        if is_new_record:
            return max_scorer_name, max_score
    return None
