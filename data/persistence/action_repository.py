from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.action import Action


@transactional
def save_action(session: Session, action: Action):
    session.add(action)
    session.commit()


@transactional
def get_action_by_event_and_blob(
    session: Session, event_id: int, blob_id: int
) -> Action | None:
    return session.query(Action).filter_by(event_id=event_id, blob_id=blob_id).first()


@transactional
def get_all_actions_by_event(session: Session, event_id: int) -> list[Action]:
    return session.query(Action).filter_by(event_id=event_id).all()


@transactional
def save_all_actions(session: Session, actions: list[Action]):
    session.add_all(actions)
    session.commit()
