import random
from data.db.db_engine import transactional
from data.model.action import Action
from data.persistence.action_repository import save_action, save_all_actions
from domain.dtos.blob_competitor_dto import BlobCompetitorDto


@transactional
def generate_score_and_save_action(contender: BlobCompetitorDto, event_id: int, tick: int, session) -> None:
    """
    Generate score for contender and save the action for given event.
    """
    score = contender.strength * random.random()
    save_action(session, Action(
        event_id=event_id,
        tick=tick,
        blob_id=contender.id,
        score=score
    ))
    return score


@transactional
def generate_and_save_all_actions(contenders: list[BlobCompetitorDto], event_id: int, tick: int, session) -> None:
    """
    Generate score for contender and save the action for given event.
    """
    actions = []
    for contender in contenders:
        score = contender.strength * random.random()
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
