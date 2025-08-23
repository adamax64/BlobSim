from sqlalchemy.orm import Session
from sqlalchemy import func, literal_column

from data.db.db_engine import transactional
from data.model.action import Action
from data.model.event_type import EventType


@transactional
def save_action(session: Session, action: Action):
    session.add(action)
    session.commit()


@transactional
def get_action_by_event_and_blob(session: Session, event_id: int, blob_id: int) -> Action | None:
    return session.query(Action).filter_by(event_id=event_id, blob_id=blob_id).first()


@transactional
def get_all_actions_by_event(session: Session, event_id: int) -> list[Action]:
    return session.query(Action).filter_by(event_id=event_id).all()


@transactional
def save_all_actions(session: Session, actions: list[Action]):
    session.add_all(actions)
    session.commit()


@transactional
def is_quartered_score_new_record(session: Session, score: float) -> bool:
    """
    Returns True if the given score is greater than all scores in actions
    where the event type is QUARTERED_ONE_SHOT_SCORING or QUARTERED_TWO_SHOT_SCORING.
    """

    # Build the query using a lateral join to unnest the scores array
    # scores_unnest = func.unnest(Action.scores).alias('score')
    query = session.query(func.max(literal_column('score')))
    query = query.select_from(
        Action,
        func.unnest(Action.scores).alias('score')
    ).join(
        Action.event
    ).filter(
        Action.event.has(
            Action.event.property.mapper.class_.type.in_([
                EventType.QUARTERED_ONE_SHOT_SCORING,
                EventType.QUARTERED_TWO_SHOT_SCORING
            ])
        )
    )
    max_score = query.scalar()
    return (max_score is None) or (score > max_score)
