from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.grandmaster import Grandmaster


@transactional
def get_all_grandmasters(session: Session) -> list[Grandmaster]:
    return session.query(Grandmaster).order_by(Grandmaster.eon.desc()).all()


@transactional
def get_grandmaster_by_eon(session: Session, eon: int) -> Grandmaster | None:
    return session.query(Grandmaster).filter(Grandmaster.eon == eon).first()


@transactional
def add_grandmaster(session: Session, grandmaster: Grandmaster) -> Grandmaster:
    session.add(grandmaster)
    session.commit()
    session.refresh(grandmaster)
    return grandmaster
