from sqlalchemy.orm import Session
from sqlalchemy import func

from data.db.db_engine import transactional
from data.model.action import Action
from data.model.event_type import EventType


@transactional
def save_action(session: Session, action: Action):
    session.add(action)
    session.commit()


@transactional
def save_all_actions(session: Session, actions: list[Action]):
    session.add_all(actions)
    session.commit()


@transactional
def actions_exist_for_event_and_tick(session: Session, event_id: int, tick: int) -> bool:
    """
    Returns True if any actions exist for the given event_id and tick, else False.
    """
    return session.query(Action).filter_by(event_id=event_id, tick=tick).first() is not None


@transactional
def is_quartered_score_new_record(session: Session, blob_id: int, score: float) -> bool:
    """
    Returns True if the given score is greater than all scores in actions
    where the event type is QUARTERED_ONE_SHOT_SCORING or QUARTERED_TWO_SHOT_SCORING.
    """
    max_score = session.query(func.max(Action.score)).join(Action.event).filter(
        Action.event.has(
            Action.event.property.mapper.class_.type.in_([
                EventType.QUARTERED_ONE_SHOT_SCORING,
                EventType.QUARTERED_TWO_SHOT_SCORING
            ])
        )
    ).scalar()
    print(f"Max score for blob {blob_id}: {max_score}, current score: {score}")
    return (max_score is None) or (score > max_score)
