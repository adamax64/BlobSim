from datetime import datetime
from sqlalchemy.exc import IntegrityError
from data.db.db_engine import transactional
from data.model.name_suggestion import NameSuggestion
from data.persistence.name_suggestion_repository import (
    get_all_name_suggestions,
    get_name_suggestion_by_id,
    save_suggestion,
)
from domain.dtos.name_suggestion_dto import NameSuggestionDto
from domain.exceptions.name_occupied_exception import NameOccupiedException


@transactional
def save_name_suggestion(session, first_name: str, last_name: str):
    try:
        save_suggestion(session, NameSuggestion(first_name=first_name, last_name=last_name, created=datetime.now()))
    except IntegrityError:
        raise NameOccupiedException()


@transactional
def get_name_suggestions(session) -> list[NameSuggestionDto]:
    return [
        NameSuggestionDto(
            id=name.id,
            first_name=name.first_name,
            last_name=name.last_name,
            created=name.created,
            parent_id=name.parent_id,
        )
        for name in get_all_name_suggestions(session)
    ]


@transactional
def update_name_suggestion(session, id: int, first_name: str):
    name_suggestion = get_name_suggestion_by_id(session, id)
    name_suggestion.first_name = first_name
    try:
        save_suggestion(session, name_suggestion)
    except IntegrityError:
        raise NameOccupiedException()
