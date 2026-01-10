from typing import List

from data.db.db_engine import transactional
from data.persistence.result_repository import get_results_of_event
from domain.dtos.result_dto import ResultDto
from domain.blob_services.blob_fetching_service import map_to_blob_state_dto
from domain.hall_of_fame_services.titles_chronology_service import get_current_grandmaster_id
from domain.sim_data_service import get_sim_time
from domain.utils.sim_time_utils import get_season


@transactional
def get_results_for_event(event_id: int, session) -> List[ResultDto]:
    """Return a list of ResultDto for a given event id."""
    results = get_results_of_event(event_id, session)

    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)
    mapped: List[ResultDto] = []
    for result in results:
        try:

            blob_dto = map_to_blob_state_dto(result.blob, current_season, grandmaster_id)
        except Exception:
            # If blob mapping fails, skip this result
            continue

        mapped.append(ResultDto(blob=blob_dto, position=result.position, points=result.points))

    return mapped
