from collections import defaultdict

from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob import Blob
from data.persistence.blob_reposiotry import get_blob_by_id
from data.persistence.calendar_repository import get_calendar
from data.persistence.result_repository import get_results_of_league_by_season
from domain.dtos.grandmaster_standings_dto import GrandmasterStandingsDTO
from domain.dtos.standings_dtos.standings_dto import StandingsDTO
from domain.dtos.standings_dtos.standings_result_dto import StandingsResultDTO
from domain.dtos.standings_dtos.standings_snippet_dto import StandingsSnippetDto
from domain.sim_data_service import get_sim_time
from domain.utils.league_utils import get_number_of_rounds_by_size
from domain.utils.sim_time_utils import get_season

_standings_cache: dict[tuple[int, int, int], list[StandingsDTO]] = {}


def invalidate_standings_cache(
    league_id: int | None = None, season: int | None = None
) -> None:
    """Drop cached standings. Omit both args to clear the entire cache."""
    if league_id is None and season is None:
        _standings_cache.clear()
        return

    for key in list(_standings_cache):
        if (league_id is None or key[0] == league_id) and (
            season is None or key[1] == season
        ):
            del _standings_cache[key]


@transactional
def get_standings(
    league_id: int, season: int, current_season: int, session: Session
) -> list[StandingsDTO]:
    cache_key = (league_id, season, current_season)
    if cache_key in _standings_cache:
        return _standings_cache[cache_key]

    results = get_results_of_league_by_season(league_id, season, session)

    if len(results) == 0:
        return []

    results_by_blob = defaultdict(list)
    for result in results:
        results_by_blob[result.blob].append(result)

    num_of_rounds = get_number_of_rounds_by_size(len(results_by_blob))

    standings = []
    for blob, results in results_by_blob.items():
        total_points = 0
        standing_results: list[StandingsResultDTO] = []
        for result in results:
            total_points += result.points
            standing_results.append(
                StandingsResultDTO(position=result.position, points=result.points)
            )

        contract_ending = season == current_season and blob.contract == current_season
        is_rookie = blob.debut == current_season and season == current_season
        standings.append(
            StandingsDTO(
                blob_id=blob.id,
                name=f"{blob.first_name} {blob.last_name}",
                color=blob.color,
                results=standing_results,
                num_of_rounds=num_of_rounds,
                total_points=total_points,
                is_contract_ending=contract_ending,
                is_rookie=is_rookie,
            )
        )

    standings.sort(key=_sort_by_position(len(standings)), reverse=True)
    _standings_cache[cache_key] = standings
    return standings


@transactional
def get_last_place_from_season_by_league(
    league_id: int, season: int, session: Session
) -> int | None:
    """Return the blob id of the last place in the standings for a given league and season.

    Returns None if no standings are available for that league/season.
    """
    standings = get_standings(league_id, season, season, session)
    if not standings:
        return None
    return standings[-1].blob_id


@transactional
def get_grandmaster_standings(
    start_season: int, current_season: int, session: Session
) -> list[GrandmasterStandingsDTO]:
    end_season = (
        current_season if start_season + 4 > current_season else start_season + 3
    )
    standings = [
        get_standings(1, season, session)
        for season in range(start_season, end_season + 1)
    ]

    is_end_season_over = (
        list(get_calendar(session).values())[-1].concluded
        or current_season != end_season
    )

    championships_by_name = defaultdict(int)
    for i, season_standings in enumerate(standings):
        if i == len(standings) - 1 and not is_end_season_over:
            continue
        championships_by_name[
            (season_standings[0].name, season_standings[0].blob_id)
        ] += 1
    standings_by_name = _get_standings_by_name(standings, championships_by_name.keys())

    grandmaster_standings = []
    for champion in championships_by_name.keys():
        results = _flatmap_results(standings_by_name[champion])
        golds = _count_by_position(results, 1)
        silvers = _count_by_position(results, 2)
        bronzes = _count_by_position(results, 3)
        points = sum(result.points for result in results)

        grandmaster_standings.append(
            GrandmasterStandingsDTO(
                blob_id=champion[1],
                name=champion[0],
                color=standings_by_name[champion][0].color,
                championships=championships_by_name[champion],
                gold=golds,
                silver=silvers,
                bronze=bronzes,
                points=points,
            )
        )
    grandmaster_standings.sort(
        key=lambda x: (x.championships, x.gold, x.silver, x.bronze, x.points),
        reverse=True,
    )
    return grandmaster_standings


@transactional
def get_standings_snippet_by_blob(
    blob_id: int, session: Session
) -> list[StandingsSnippetDto]:
    """Fetch the standings of the referenced blob and the competitors before and after them.

    Returns a list of three StandingsSnippetDto objects, ordered by position.
    If the blob is in first or last place, the list will contain only two objects.
    """

    season = get_season(get_sim_time())

    blob = get_blob_by_id(session, blob_id)
    if not blob or not blob.league:
        return []

    standings = get_standings(blob.league.id, season, season, session)
    snippet = []
    for i, standing in enumerate(standings):
        if standing.blob_id == blob_id:
            if i > 0:
                snippet.append(
                    StandingsSnippetDto(
                        blob_id=standings[i - 1].blob_id,
                        blob_name=standings[i - 1].name,
                        blob_color=standings[i - 1].color,
                        position=i,
                        points=standings[i - 1].total_points,
                    )
                )
            snippet.append(
                StandingsSnippetDto(
                    blob_id=standing.blob_id,
                    blob_name=standing.name,
                    blob_color=standing.color,
                    position=i + 1,
                    points=standing.total_points,
                )
            )
            if i < len(standings) - 1:
                snippet.append(
                    StandingsSnippetDto(
                        blob_id=standings[i + 1].blob_id,
                        blob_name=standings[i + 1].name,
                        blob_color=standings[i + 1].color,
                        position=i + 2,
                        points=standings[i + 1].total_points,
                    )
                )
            break
    return snippet


@transactional
def get_standings_by_league(
    session: Session, blobs: list[Blob], season: int
) -> dict[int, dict[int, int]]:
    """
    Fetch standings for all leagues of the given blobs.

    Returns a dictionary mapping league_id -> {blob_id -> position}
    """
    from domain.standings_service import get_standings

    standings_by_league = {}
    for blob in blobs:
        if blob.league and blob.league.id not in standings_by_league:
            standings = get_standings(
                session=session,
                league_id=blob.league.id,
                season=season,
                current_season=season,
            )
            standings_by_league[blob.league.id] = {
                standing.blob_id: idx + 1 for idx, standing in enumerate(standings)
            }
    return standings_by_league


def _get_standings_by_name(
    standings: list[list[StandingsDTO]], champions: list[tuple[str, int]]
) -> dict[str, list[StandingsDTO]]:
    standings_by_name = {}
    for standing_record in standings:
        for standing in standing_record:
            key = (standing.name, standing.blob_id)
            if key in standings_by_name:
                standings_by_name[key].append(standing)
            elif key in champions:
                standings_by_name[key] = [standing]
    return standings_by_name


def _flatmap_results(standings: list[StandingsDTO]) -> list[StandingsResultDTO]:
    return [result for standing in standings for result in standing.results]


def _count_by_position(results: list[StandingsResultDTO], position: int) -> int:
    return len([result for result in results if result.position == position])


def _sort_by_position(field_size: int):
    return lambda x: (
        x.total_points,
        *(_count_by_position(x.results, i + 1) for i in range(field_size)),
    )
