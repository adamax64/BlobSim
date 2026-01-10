from data.db.db_engine import transactional
from data.persistence.blob_reposiotry import get_all_blobs_by_name
from data.persistence.champion_repository import get_all_champions
from data.persistence.grandmaster_repository import get_all_grandmasters
from domain.dtos.titles_count_dto import TitleCountDto, TitlesCountSummaryDto
from domain.hall_of_fame_services.titles_chronology_service import get_current_grandmaster_id
from domain.sim_data_service import get_sim_time
from domain.utils.blob_utils import map_to_blob_state_dto
from domain.utils.sim_time_utils import get_season


@transactional
def get_titles_count(session) -> TitlesCountSummaryDto:
    """
    Return the count of the following:
    - Grandmaster titles
    - Top league championships
    - Top league wins
    - Top league podiums
    - Lower league season victories
    - Lower league wins
    - Lower league podiums
    """

    current_season = get_season(get_sim_time(session))
    grandmaster_id = get_current_grandmaster_id(session)

    blobs = get_all_blobs_by_name(session=session, name_search=None, show_dead=True)

    return TitlesCountSummaryDto(
        grandmasters=_get_grandmaster_counts(session, current_season, grandmaster_id),
        championships=_get_champion_counts(session, current_season, grandmaster_id, blobs),
        top_wins=_get_top_win_counts(current_season, grandmaster_id, blobs),
        top_podiums=_get_top_podium_counts(current_season, grandmaster_id, blobs),
        season_victories=_get_lower_victory_counts(current_season, grandmaster_id, blobs),
        lower_wins=_get_lower_win_counts(current_season, grandmaster_id, blobs),
        lower_podiums=_get_lower_podium_counts(current_season, grandmaster_id, blobs),
        )


def _get_grandmaster_counts(session, current_season: int, grandmaster_id: int) -> list[TitleCountDto]:
    grandmasters = get_all_grandmasters(session)
    grandmaster_counts = {}
    for gm in grandmasters:
        if gm.blob not in grandmaster_counts:
            grandmaster_counts[gm.blob] = 0
        grandmaster_counts[gm.blob] += 1
    return [
        TitleCountDto(
            blob=map_to_blob_state_dto(blob, current_season, grandmaster_id),
            count=count
        )
        for blob, count in grandmaster_counts.items()
    ]


def _get_champion_counts(session, current_season: int, grandmaster_id: int, blobs) -> list[TitleCountDto]:
    champions = get_all_champions(session)
    champion_counts = {}
    for champ in champions:
        if champ.blob not in champion_counts:
            champion_counts[champ.blob] = 0
        champion_counts[champ.blob] += 1
    return [
        TitleCountDto(
            blob=map_to_blob_state_dto(blob, current_season, grandmaster_id),
            count=count
        )
        for blob, count in champion_counts.items()
    ]


def _get_top_win_counts(current_season: int, grandmaster_id: int, blobs) -> list[TitleCountDto]:
    blobs_sorted = sorted(blobs, key=lambda b: b.gold_trophies, reverse=True)
    return [
        TitleCountDto(
            blob=map_to_blob_state_dto(blob, current_season, grandmaster_id),
            count=blob.gold_trophies
        )
        for blob in blobs_sorted if blob.gold_trophies > 0
    ]


def _get_top_podium_counts(current_season: int, grandmaster_id: int, blobs) -> list[TitleCountDto]:
    blobs_sorted = sorted(blobs, key=lambda b: b.bronze_trophies + b.silver_trophies + b.gold_trophies, reverse=True)
    return [
        TitleCountDto(
            blob=map_to_blob_state_dto(blob, current_season, grandmaster_id),
            count=blob.bronze_trophies + blob.silver_trophies + blob.gold_trophies
        )
        for blob in blobs_sorted if (blob.bronze_trophies + blob.silver_trophies + blob.gold_trophies) > 0
    ]


def _get_lower_victory_counts(current_season: int, grandmaster_id: int, blobs) -> list[TitleCountDto]:
    blobs_sorted = sorted(blobs, key=lambda b: b.season_victories, reverse=True)
    return [
        TitleCountDto(
            blob=map_to_blob_state_dto(blob, current_season, grandmaster_id),
            count=blob.season_victories
        )
        for blob in blobs_sorted if blob.season_victories > 0
    ]


def _get_lower_win_counts(current_season: int, grandmaster_id: int, blobs) -> list[TitleCountDto]:
    blobs_sorted = sorted(blobs, key=lambda b: b.gold_medals, reverse=True)
    return [
        TitleCountDto(
            blob=map_to_blob_state_dto(blob, current_season, grandmaster_id),
            count=blob.gold_medals
        )
        for blob in blobs_sorted if blob.gold_medals > 0
    ]


def _get_lower_podium_counts(current_season: int, grandmaster_id: int, blobs) -> list[TitleCountDto]:
    blobs_sorted = sorted(blobs, key=lambda b: b.bronze_medals + b.silver_medals + b.gold_medals, reverse=True)
    return [
        TitleCountDto(
            blob=map_to_blob_state_dto(blob, current_season, grandmaster_id),
            count=blob.bronze_medals + blob.silver_medals + blob.gold_medals
        )
        for blob in blobs_sorted if (blob.bronze_medals + blob.silver_medals + blob.gold_medals) > 0
    ]
