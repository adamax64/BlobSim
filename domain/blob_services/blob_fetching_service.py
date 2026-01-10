from data.db.db_engine import transactional
from data.model.blob import Blob
from data.persistence.blob_reposiotry import (
    get_all_blobs_by_name,
    get_blob_by_id,
)
from domain.dtos.blob_stats_dto import BlobStatsDto
from domain.hall_of_fame_services.titles_chronology_service import get_current_grandmaster_id
from domain.sim_data_service import get_sim_time
from domain.utils.blob_utils import map_to_blob_state_dto
from domain.utils.sim_time_utils import get_season


@transactional
def fetch_all_blobs(
    session, name_search: str = None, show_dead: bool = False
) -> list[BlobStatsDto]:
    """Get all living blobs and return them as a list of BlobStatsDto."""

    blobs: list[Blob] = get_all_blobs_by_name(
        session=session, name_search=name_search, show_dead=show_dead
    )

    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)

    return [
        map_to_blob_state_dto(blob, current_season, grandmaster_id)
        for blob in blobs
    ]


@transactional
def fetch_blob_by_id(blob_id: int, session) -> BlobStatsDto:
    """Fetch a blob by its ID and return it as a BlobStatsDto."""

    current_season = get_season(get_sim_time(session))
    blob = get_blob_by_id(session, blob_id)
    grandmaster_id = get_current_grandmaster_id(session)

    if not blob:
        raise ValueError(f"Blob with ID {blob_id} not found")

    return map_to_blob_state_dto(blob, current_season, grandmaster_id)
