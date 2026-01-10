from data.db.db_engine import transactional
from domain.dtos.titles_chronology_dto import ChampionDto, GrandmasterDto, LeagueChampionsDto, TitlesChronologyDto

from data.persistence.champion_repository import get_all_champions
from data.persistence.grandmaster_repository import get_all_grandmasters, get_grandmaster_by_eon
from domain.sim_data_service import get_sim_time
from domain.utils.blob_utils import map_to_blob_state_dto
from domain.utils.league_utils import map_league_to_dto
from domain.utils.sim_time_utils import get_eon, get_season


@transactional
def get_current_grandmaster_id(session) -> int | None:
    """Return the blob ID of the current grandmaster, or None if there is no grandmaster."""
    current_time = get_sim_time(session)
    current_eon = get_eon(current_time)
    grandmaster = get_grandmaster_by_eon(session, current_eon)
    if grandmaster:
        return grandmaster.blob_id
    return None


@transactional
def get_titles_chronology(session) -> TitlesChronologyDto:
    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)

    return TitlesChronologyDto(
        league_champions=_get_champions_per_league(session, current_season, grandmaster_id),
        grandmasters=_get_grandmasters_list(session, current_season, grandmaster_id)
    )


def _get_champions_per_league(session, current_season: int, grandmaster_id: int) -> list[LeagueChampionsDto]:
    champions = get_all_champions(session)

    league_champions: list[LeagueChampionsDto] = []
    for champion in champions:
        league_dto = map_league_to_dto(champion.league, champion.league.players)
        blob_stats_dto = map_to_blob_state_dto(champion.blob, current_season, grandmaster_id)
        champion_dto = ChampionDto(
            season=champion.season,
            blob=blob_stats_dto
        )
        if league_dto not in [lc.league for lc in league_champions]:
            league_champions.append(LeagueChampionsDto(league=league_dto, champions=[]))
        league_champions[[lc.league for lc in league_champions].index(league_dto)].champions.append(champion_dto)

    return league_champions


def _get_grandmasters_list(session, current_season: int, grandmaster_id: int) -> list[GrandmasterDto]:
    grandmasters = get_all_grandmasters(session)

    grandmasters_list: list[GrandmasterDto] = []
    for grandmaster in grandmasters:
        blob_stats_dto = map_to_blob_state_dto(grandmaster.blob, current_season, grandmaster_id)
        grandmaster_dto = GrandmasterDto(
            eon=grandmaster.eon,
            blob=blob_stats_dto
        )
        grandmasters_list.append(grandmaster_dto)

    return grandmasters_list
