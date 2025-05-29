from collections import defaultdict

from data.db.db_engine import transactional
from data.persistence.calendar_repository import get_calendar
from data.persistence.result_repository import get_results_of_league_by_season
from domain.dtos.grandmaster_standings_dto import GrandmasterStandingsDTO
from domain.dtos.standings_dto import StandingsDTO
from domain.dtos.standings_result_dto import StandingsResultDTO
from domain.utils.league_utils import get_number_of_rounds_by_size


@transactional
def get_standings(league_id: int, season: int, current_season: int, session) -> list[StandingsDTO]:
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
            standing_results.append(StandingsResultDTO(position=result.position, points=result.points))

        contract_ending = season == current_season and blob.contract == current_season
        standings.append(StandingsDTO(
            blob_id=blob.id,
            name=f"{blob.first_name} {blob.last_name}",
            results=standing_results,
            num_of_rounds=num_of_rounds,
            total_points=total_points,
            is_contract_ending=contract_ending
        ))

    standings.sort(key=_sort_by_position(len(standings)), reverse=True)
    return standings


@transactional
def get_grandmaster_standings(start_season: int, current_season: int, session) -> list[GrandmasterStandingsDTO]:
    end_season = current_season if start_season + 4 > current_season else start_season + 3
    standings = [get_standings(1, season, session) for season in range(start_season, end_season + 1)]

    is_current_season_over = list(get_calendar(session).values())[-1].concluded

    championships_by_name = defaultdict(int)
    for i, season_standings in enumerate(standings):
        if i == len(standings) - 1 and not is_current_season_over:
            continue
        championships_by_name[(season_standings[0].name, season_standings[0].blob_id)] += 1
    standings_by_name = _get_standings_by_name(standings, championships_by_name.keys())

    grandmaster_standings = []
    for champion in championships_by_name.keys():
        results = _flatmap_results(standings_by_name[champion])
        golds = _count_by_position(results, 1)
        silvers = _count_by_position(results, 2)
        bronzes = _count_by_position(results, 3)
        points = sum(result.points for result in results)

        grandmaster_standings.append(GrandmasterStandingsDTO(
            blob_id=champion[1],
            name=champion[0],
            championships=championships_by_name[champion],
            gold=golds,
            silver=silvers,
            bronze=bronzes,
            points=points
        ))
    grandmaster_standings.sort(key=lambda x: (x.championships, x.gold, x.silver, x.bronze, x.points), reverse=True)
    return grandmaster_standings


def _get_standings_by_name(standings: list[list[StandingsDTO]], champions: list[tuple[str, int]]) -> dict[str, list[StandingsDTO]]:
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
        x.total_points, *(_count_by_position(x.results, i + 1) for i in range(field_size))
    )
