import random
from data.db.db_engine import transactional
from data.model.action import Action
from data.persistence.action_repository import save_action
from domain.dtos.blob_competitor_dto import BlobCompetitorDto


@transactional
def generate_score_and_save_action(contender: BlobCompetitorDto, event_id: int, tick: int, session) -> float:
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
