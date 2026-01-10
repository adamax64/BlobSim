from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.champion import Champion


@transactional
def get_all_champions(session: Session) -> list[Champion]:
    return session.query(Champion).order_by(Champion.season.desc()).all()


@transactional
def add_champion(session: Session, champion: Champion) -> Champion:
    session.add(champion)
    session.commit()
    session.refresh(champion)
    return champion
