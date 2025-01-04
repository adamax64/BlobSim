from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.action import Action


@transactional
def save_action(session: Session, action: Action):
    session.add(action)
    session.commit()
