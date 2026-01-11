from data.persistence.record_repository import (
    get_all_records,
    is_score_new_record,
    update_record_if_better
)
from data.model.event_type import EventType
from domain.dtos.league_dto import LeagueDto
from domain.dtos.record_dto import RecordDto
from data.db.db_engine import transactional
from domain.hall_of_fame_services.titles_chronology_service import get_current_grandmaster_id
from domain.sim_data_service import get_sim_time
from domain.utils.blob_utils import map_to_blob_state_dto
from domain.utils.sim_time_utils import get_season


@transactional
def get_all_records_service(session) -> list[RecordDto]:
    """Get all records in the system."""

    # Determine current season and grandmaster id for BlobStats mapping
    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)

    records = get_all_records(session)
    return [
        RecordDto(
            id=record.id,
            league=LeagueDto(
                id=record.league.id,
                name=record.league.name,
                field_size=len(record.league.players),
                level=record.league.level
            ),
            event_type=record.event_type,
            blob=map_to_blob_state_dto(record.competitor, current_season, grandmaster_id),
            score=record.score
        )
        for record in records
    ]


@transactional
def check_and_update_record(league_id: int, event_type: EventType, competitor_id: int, score: float, session) -> bool:
    """
    Check if a score is a new record and update if it is.
    Returns True if a new record was set, False otherwise.
    """
    return update_record_if_better(session, league_id, event_type, competitor_id, score)


@transactional
def is_new_record(league_id: int, event_type: EventType, score: float, session) -> bool:
    """Check if a score would be a new record without updating."""
    return is_score_new_record(session, league_id, event_type, score)
