from data.db.db_engine import transactional
from data.model.blob import Blob
from data.persistence.blob_reposiotry import (
    get_all_blobs_by_name,
    get_blob_by_id,
    get_blob_relative_speeds_by_blob,
    get_blob_relative_strengths_by_blob,
)
from domain.dtos.blob_stats_dto import BlobStatsDto, IntegrityState, SpeedCategory, StrengthCategory
from domain.dtos.parent_dto import ParentDto
from domain.sim_data_service import get_sim_time
from domain.utils.blob_name_utils import format_blob_name
from domain.utils.constants import INITIAL_INTEGRITY
from domain.utils.sim_time_utils import format_sim_time_short, get_season


@transactional
def fetch_all_blobs(
    session, name_search: str = None, show_dead: bool = False
) -> list[BlobStatsDto]:
    """Get all living blobs and return them as a list of BlobStatsDto."""

    blobs: list[Blob] = get_all_blobs_by_name(
        session=session, name_search=name_search, show_dead=show_dead
    )

    current_season = get_season(get_sim_time(session))

    relative_strengths = get_blob_relative_strengths_by_blob(session)
    relative_speeds = get_blob_relative_speeds_by_blob(session)

    return [
        _map_to_blob_state_dto(blob, current_season, relative_speeds.get(blob.id, 0), relative_strengths.get(blob.id, 0))
        for blob in blobs
    ]


@transactional
def fetch_blob_by_id(blob_id: int, session) -> BlobStatsDto:
    """Fetch a blob by its ID and return it as a BlobStatsDto."""

    current_season = get_season(get_sim_time(session))

    relative_strengths = get_blob_relative_strengths_by_blob(session)
    relative_speeds = get_blob_relative_speeds_by_blob(session)

    blob = get_blob_by_id(session, blob_id)

    if not blob:
        raise ValueError(f"Blob with ID {blob_id} not found")

    return _map_to_blob_state_dto(blob, current_season, relative_speeds.get(blob.id, 0), relative_strengths.get(blob.id, 0))


def _map_to_blob_state_dto(blob: Blob, current_season: int, relative_speed: float, relative_strength: float) -> BlobStatsDto:
    return BlobStatsDto(
            name=format_blob_name(blob),
            born=format_sim_time_short(blob.born),
            terminated=format_sim_time_short(blob.terminated) if blob.terminated else None,
            debut=blob.debut,
            contract=blob.contract,
            podiums=(blob.bronze_trophies + blob.silver_trophies + blob.gold_trophies),
            wins=blob.gold_trophies,
            championships=blob.championships,
            grandmasters=blob.grandmasters,
            league_name=blob.league.name if blob.league else "None",
            is_rookie=blob.debut == current_season,
            at_risk=blob.contract == current_season,
            is_dead=blob.terminated is not None,
            is_retired=blob.contract is not None and blob.contract < current_season,
            color=blob.color,
            parent=ParentDto(name=format_blob_name(blob.parent), color=blob.parent.color) if blob.parent else None,
            money=blob.money if blob.integrity > 0 else None,
            speed_category=(
                SpeedCategory.FAST
                if relative_speed > 0.66
                else SpeedCategory.AVERAGE
                if relative_speed > 0.33
                else SpeedCategory.SLOW
            ) if blob.integrity > 0 else None,
            strength_category=(
                StrengthCategory.STRONG
                if relative_strength > 0.66
                else StrengthCategory.AVERAGE
                if relative_strength > 0.33
                else StrengthCategory.WEAK
            ) if blob.integrity > 0 else None,
            integrity_state=(
                IntegrityState.GOOD
                if blob.integrity > 0.7
                else IntegrityState.AVERAGE
                if blob.integrity > 0.4
                else IntegrityState.POOR
            ) if blob.integrity > 0 else None,
            speed_color=_get_color_indicator(relative_speed) if blob.integrity > 0 else None,
            strength_color=_get_color_indicator(relative_strength) if blob.integrity > 0 else None,
            integrity_color=_get_color_indicator(blob.integrity / INITIAL_INTEGRITY) if blob.integrity > 0 else None,
            current_activity=blob.current_activity if blob.integrity > 0 and blob.current_activity is not None else None,
        )


def _get_color_indicator(relative_value: float) -> str:
    """Get a color indicator (red, yellow, green) based on the relative value of a blob's attribute."""
    red = int(min(255, max(0, 255 * (2 - 2 * relative_value))))
    green = int(min(255, max(0, 255 * (2 * relative_value))))
    blue = 0
    return f"#{red:02x}{green:02x}{blue:02x}"
