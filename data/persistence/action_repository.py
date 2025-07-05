from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.action import Action


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
