from typing import List

from data.db.db_engine import transactional
from data.persistence.event_repository import get_events_by_season
from data.persistence.result_repository import get_results_of_event
from domain.dtos.result_dto import ResultDto
from domain.dtos.season_competition_dto import SeasonCompetitionDto
from domain.utils.blob_utils import map_to_blob_state_dto
from domain.hall_of_fame_services.titles_chronology_service import (
    get_current_grandmaster_id,
)
from domain.sim_data_service import get_sim_time
from domain.standings_service import get_standings_by_league
from domain.utils.sim_time_utils import convert_to_sim_time, get_season


@transactional
def get_results_for_event(event_id: int, session) -> List[ResultDto]:
    """Return a list of ResultDto for a given event id."""
    results = get_results_of_event(event_id, session)

    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)

    # Build standings position map for blobs
    result_blobs = [result.blob for result in results]
    standings_by_league = get_standings_by_league(session, result_blobs, current_season)

    mapped: List[ResultDto] = []
    for result in results:
        try:
            standings_position = None
            if result.blob.league:
                standings_position = standings_by_league.get(
                    result.blob.league.id, {}
                ).get(result.blob.id)

            blob_dto = map_to_blob_state_dto(
                result.blob, current_season, grandmaster_id, standings_position
            )
        except Exception:
            # If blob mapping fails, skip this result
            continue

        mapped.append(
            ResultDto(blob=blob_dto, position=result.position, points=result.points)
        )

    return mapped


@transactional
def get_competitions_by_season(season: int, session) -> List[SeasonCompetitionDto]:
    """Return all competitions (events) for the given season, ordered by date."""
    events = get_events_by_season(session, season, exclude_non_competition=True)
    sorted_events = sorted(events, key=lambda e: e.date, reverse=True)
    return [
        SeasonCompetitionDto(
            id=event.id,
            date=convert_to_sim_time(event.date),
            league_name=event.league.name if event.league else "",
            round=event.round,
            event_type=event.type,
        )
        for event in sorted_events
    ]
