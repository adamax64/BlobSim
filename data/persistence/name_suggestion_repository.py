from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.name_suggestion import NameSuggestion


@transactional
def save_suggestion(session: Session, name: NameSuggestion):
    session.merge(name)
    session.commit()


@transactional
def get_name_suggestion_by_id(session: Session, id: int) -> NameSuggestion:
    return session.query(NameSuggestion).filter(NameSuggestion.id == id).first()


@transactional
def get_all_name_suggestions(session: Session) -> list[NameSuggestion]:
    return session.query(NameSuggestion).order_by(
        NameSuggestion.parent_id.is_(None),
        NameSuggestion.created
    ).all()


@transactional
def get_oldest_name(session: Session) -> NameSuggestion:
    return session.query(NameSuggestion).order_by(
        NameSuggestion.parent_id.is_(None),
        NameSuggestion.created
    ).first()


@transactional
def delete_suggestion(session: Session, name: NameSuggestion):
    session.delete(name)
    session.commit()
