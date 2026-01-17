from data.db.db_engine import transactional
from domain.dtos.records_by_event_dto import (
    RecordsByEventDto,
    RecordsByLeagueDto,
    WinsByEventDto,
)
from domain.record_service import get_all_records_service
from domain.standings_service import get_standings_by_league
from domain.utils.blob_utils import map_to_blob_state_dto
from domain.sim_data_service import get_sim_time
from domain.utils.sim_time_utils import get_season
from domain.hall_of_fame_services.titles_chronology_service import (
    get_current_grandmaster_id,
)
from data.persistence.result_repository import get_wins_by_event
from data.persistence.blob_reposiotry import get_all_by_ids


@transactional
def get_records_by_event_type(session) -> RecordsByEventDto:
    """Fetch wins and records organized by event type and league."""

    return RecordsByEventDto(
        winsByEvent=_get_wins_by_event(session),
        recordsByLeague=_get_records_by_league(session),
    )


def _get_records_by_league(session) -> list[RecordsByLeagueDto]:
    """Fetch all records and organize them by event type and league."""
    records = get_all_records_service(session)

    records_by_event: dict = {}
    for record in records:
        if record.league.level not in records_by_event:
            records_by_event[record.league.level] = []
        records_by_event[record.league.level].append(record)

    mapped = [
        RecordsByLeagueDto(
            league=records_by_event[level][0].league, records=records_by_event[level]
        )
        for level in sorted(records_by_event.keys())
    ]

    return mapped


def _get_wins_by_event(session) -> list[WinsByEventDto]:
    """Fetch wins by event type."""
    # Count wins (position == 1) per event type and blob (delegated to repository)
    rows = get_wins_by_event(session)

    # Determine current season and grandmaster id for BlobStats mapping
    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)

    best: dict = {}
    for event_type, blob_id, wins in rows:
        key = event_type
        if (
            key not in best
            or wins > best[key][1]
            or (wins == best[key][1] and blob_id < best[key][0])
        ):
            best[key] = (blob_id, wins)

    # Fetch all blobs at once
    blob_ids = [blob_id for _, (blob_id, _) in best.items()]
    blobs = get_all_by_ids(session, blob_ids)
    blobs_by_id = {blob.id: blob for blob in blobs}

    standings_by_league = get_standings_by_league(session, blobs, current_season)

    result: list[WinsByEventDto] = []
    for event_type, (blob_id, wins) in best.items():
        blob = blobs_by_id.get(blob_id)
        if not blob:
            continue

        standings_position = (
            standings_by_league.get(blob.league.id, {}).get(blob.id)
            if blob.league
            else None
        )
        blob_dto = map_to_blob_state_dto(
            blob, current_season, grandmaster_id, standings_position
        )
        result.append(WinsByEventDto(event_type, blob_dto, wins))

    return result
