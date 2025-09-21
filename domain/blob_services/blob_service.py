from dataclasses import dataclass

from data.db.db_engine import transactional
from domain.blob_services.blob_fetching_service import fetch_all_blobs
from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.blob_services.blob_creation_service import create_blob as service_create_blob
from domain.blob_services.blob_update_service import update_all_blobs


@dataclass
class StatMultiplyers:
    strength: float
    speed: float


@transactional
def get_all_blobs(
    session, name_search: str = None, show_dead: bool = False
) -> list[BlobStatsDto]:
    """Get all blobs and return them as a list of BlobStatsDto."""
    return fetch_all_blobs(
        session=session, name_search=name_search, show_dead=show_dead
    )


@transactional
def create_blob(session, first_name: str, last_name: str, parent_id: int | None = None):
    """Create a new blob with random stats and add it to the queue."""
    service_create_blob(session, first_name, last_name, parent_id)


@transactional
def update_blobs(session):
    """Update all blobs living in the simulation and yield the progress in percentage."""
    update_all_blobs(session)
