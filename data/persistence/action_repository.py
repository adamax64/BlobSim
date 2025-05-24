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
