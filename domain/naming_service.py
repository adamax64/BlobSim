from datetime import datetime
from sqlalchemy.exc import IntegrityError
from data.db.db_engine import transactional
from data.model.name_suggestion import NameSuggestion
from data.persistence.name_suggestion_repository import save_suggestion
from domain.exceptions.name_occupied_exception import NameOccupiedException


@transactional
def save_name_suggestion(session, name: str):
    try:
        save_suggestion(session, NameSuggestion(name=name, created=datetime.now()))
    except IntegrityError:
        raise NameOccupiedException()
