from math import ceil
from typing import List
from data.db.db_engine import transactional
from data.persistence.blob_reposiotry import get_all_by_league_order_by_id, get_blob_by_id, save_all_blobs, save_blob
from data.persistence.calendar_repository import count_unconcluded_for_league
from domain.dtos.grandmaster_standings_dto import GrandmasterStandingsDTO
from domain.dtos.league_dto import LeagueDto
from domain.dtos.standings_dto import StandingsDTO
from domain.standings_service import get_grandmaster_standings, get_standings
from domain.utils.constants import CHAMPION_PRIZE, CYCLES_PER_EON, GRANDMASTER_PRIZE


@transactional
def end_eon_if_over(season: int, league: LeagueDto, session) -> List[GrandmasterStandingsDTO]:
    if not league.level == 1 or not season % 4 == 0 or count_unconcluded_for_league(session, league.id) > 0:
        return None

    grandmaster_standings: List[GrandmasterStandingsDTO] = get_grandmaster_standings(season - 3, season, session)
    grandmaster = get_blob_by_id(session, grandmaster_standings[0].blob_id)
    grandmaster.grandmasters += 1
    grandmaster.money += GRANDMASTER_PRIZE
    if grandmaster.integrity < CYCLES_PER_EON:
        grandmaster.integrity = CYCLES_PER_EON
    save_blob(session, grandmaster)

    return grandmaster_standings


@transactional
def end_season_if_over(league: LeagueDto, season: int, session) -> List[StandingsDTO]:
    if count_unconcluded_for_league(session, league.id) > 0:
        return None

    standings: List[StandingsDTO] = get_standings(league.id, season, session)
    blobs = get_all_by_league_order_by_id(session, league.id)
    for i, standing in enumerate(standings):
        extension = _calculate_contract_extension(i + 1, len(standings))
        blob = blobs[standing.blob_id]
        blob.contract += extension
        if i == 0 and league.level == 1:
            blob.championships += 1
            blob.money += CHAMPION_PRIZE
        elif i == 0:
            blob.season_victories += 1
            blob.money += CHAMPION_PRIZE

    save_all_blobs(session, list(blobs.values()))
    return standings


def _calculate_contract_extension(position: int, field_size: int) -> int:
    result = 0
    half_point = ceil(field_size / 2)
    quarter_point = ceil(field_size / 4)
    if position <= half_point:
        result += 1
    if position <= quarter_point and field_size >= 19:
        result += 1
    if position <= 3 and field_size >= 11:
        result += 1
    if position == 1:
        result += 1

    return result
