from data.model.blob import Blob
from data.model.state_type import StateType
from domain.dtos.blob_stats_dto import BlobStatsDto, IntegrityState
from domain.dtos.parent_dto import ParentDto
from domain.dtos.state_dto import StateDto
from domain.utils.constants import INITIAL_INTEGRITY
from domain.utils.sim_time_utils import format_sim_time_short
from data.model.trait_type import TraitType


def has_trait(blob: Blob, trait_type: TraitType) -> bool:
    """Return True if `blob.traits` contains a trait of given `trait_type`."""
    return any(t.type == trait_type for t in blob.traits)


def has_state(blob: Blob, state_type: StateType) -> bool:
    """Return True if `blob.states` contains a state of given `state_type`."""
    return any(s.type == state_type for s in blob.states)


def compute_state_multiplier(blob: Blob, current_time: int) -> float:
    """Compute the multiplicative modifier for training effects based on active states.

    Multipliers:
      - INJURED: *0.2 (-80%)
      - TIRED: *0.5 (-50%)
      - GLOOMY: *0.85 (-15%)
      - FOCUSED: *1.2 (+20%)

    States stack multiplicatively.
    """
    multiplier = 1.0
    if blob is None:
        return multiplier
    for st in blob.states or []:
        if st.effect_until < current_time:
            continue
        st_type: StateType = st.type
        if st_type == StateType.INJURED:
            multiplier *= 0.2
        elif st_type == StateType.TIRED:
            multiplier *= 0.5
        elif st_type == StateType.GLOOMY:
            multiplier *= 0.85
        elif st_type == StateType.FOCUSED:
            multiplier *= 1.2
    return multiplier


def format_blob_name(blob) -> str:
    first = blob.first_name.strip() if blob.first_name else ""
    last = blob.last_name.strip() if blob.last_name else ""
    return f"{first} {last}".strip()


def map_to_blob_state_dto(
    blob: Blob,
    current_season: int,
    grandmaster_id: int,
    standings_position: int | None,
) -> BlobStatsDto:
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
        is_grandmaster=grandmaster_id == blob.id,
        color=blob.color,
        parent=(
            ParentDto(name=format_blob_name(blob.parent), color=blob.parent.color)
            if blob.parent
            else None
        ),
        money=blob.money if blob.integrity > 0 else None,
        integrity_state=(
            (
                IntegrityState.GOOD
                if blob.integrity > 0.7
                else (
                    IntegrityState.AVERAGE
                    if blob.integrity > 0.4
                    else IntegrityState.POOR
                )
            )
            if blob.integrity > 0
            else None
        ),
        integrity_color=(
            _get_color_indicator(blob.integrity / INITIAL_INTEGRITY)
            if blob.integrity > 0
            else None
        ),
        current_activity=(
            blob.current_activity
            if blob.integrity > 0 and blob.current_activity is not None
            else None
        ),
        current_standings_position=standings_position,
        states=[
            StateDto(
                type=state.type,
                effect_until=format_sim_time_short(state.effect_until),
            )
            for state in blob.states
        ],
    )


def _get_color_indicator(relative_value: float) -> str:
    """Get a color indicator (red, yellow, green) based on the relative value of a blob's attribute."""
    red = int(min(255, max(0, 255 * (2 - 2 * relative_value))))
    green = int(min(255, max(0, 255 * (2 * relative_value))))
    blue = 0
    return f"#{red:02x}{green:02x}{blue:02x}"
