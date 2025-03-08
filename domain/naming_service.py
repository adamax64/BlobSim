from datetime import datetime
from sqlalchemy.exc import IntegrityError
from data.db.db_engine import transactional
from data.model.name_suggestion import NameSuggestion
from data.persistence.name_suggestion_repository import (
    get_all_name_suggestions,
    save_suggestion,
)
from domain.dtos.name_suggestion_dto import NameSuggestionDto
from domain.exceptions.name_occupied_exception import NameOccupiedException


@transactional
def save_name_suggestion(session, name: str):
    try:
        save_suggestion(session, NameSuggestion(name=name, created=datetime.now()))
    except IntegrityError:
        raise NameOccupiedException()


@transactional
def get_name_suggestions(session) -> list[NameSuggestionDto]:
    return [
        NameSuggestionDto(id=name.id, name=name.name, created=name.created)
        for name in get_all_name_suggestions(session)
    ]
