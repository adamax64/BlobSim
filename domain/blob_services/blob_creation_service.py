from logging import warning
import random

from psycopg2 import IntegrityError
from data.db.db_engine import transactional
from data.model.blob import Blob
from data.persistence.blob_reposiotry import get_blob_by_id, save_blob
from data.persistence.league_repository import get_queue
from data.persistence.name_suggestion_repository import delete_suggestion, get_oldest_name
from domain.exceptions.name_occupied_exception import NameOccupiedException
from domain.news_services.news_service import add_blob_created_news, add_blob_in_creation_news
from domain.sim_data_service import get_sim_time, is_blob_created, reset_factory_progress
from domain.utils.blob_name_utils import format_blob_name
from domain.utils.color_utils import generate_random_color
from domain.utils.constants import INITIAL_INTEGRITY


@transactional
def check_factory_and_create_blob(session):
    if is_blob_created(session):
        _create_with_name_suggestion(session)


@transactional
def create_blob(session, first_name: str, last_name: str, parent_id: int | None = None):
    """Create a new blob with random stats and add it to the queue."""

    strength = 0.9 + random.random() * 0.2
    speed = 0.9 + random.random() * 0.2
    learning = 0.5 + 0.5 * random.random()
    current_time = get_sim_time(session)
    queue = get_queue(session)

    if parent_id is not None:
        parent = get_blob_by_id(session, parent_id)
        learning += parent.championships * 0.01
        strength += parent.grandmasters * 0.01
        speed += parent.grandmasters * 0.01

    try:
        save_blob(
            session,
            Blob(
                first_name=first_name,
                last_name=last_name,
                strength=strength,
                speed=speed,
                learning=learning,
                integrity=INITIAL_INTEGRITY,
                born=current_time,
                league_id=queue.id,
                parent_id=parent_id,
                color=generate_random_color(),
            ),
        )
        reset_factory_progress(session)
        add_blob_created_news(f'{first_name} {last_name}', session)
    except IntegrityError:
        raise NameOccupiedException()


@transactional
def _create_with_name_suggestion(session):
    """Try to create new blob with suggested names. Retry if there is already a blob with suggested name"""

    name_suggestion = get_oldest_name(session)
    if name_suggestion is None:
        add_blob_in_creation_news(session)
        return
    try:
        create_blob(session, name_suggestion.first_name, name_suggestion.last_name, name_suggestion.parent_id)
        delete_suggestion(session, name_suggestion)
        format_blob_name(name_suggestion)
    except NameOccupiedException:
        session.close()
        warning("There already exists a blob with suggested name, retrying creating blob...")
        delete_suggestion(name=name_suggestion)
        _create_with_name_suggestion()
