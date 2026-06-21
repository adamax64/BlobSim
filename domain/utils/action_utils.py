import random
from functools import lru_cache

from domain.dtos.blob_competitor_dto import BlobCompetitorDto
from domain.utils.item_utils import (
    PRE_EVENT_MIN_SCORE_STATE_BONUSES,
    PRE_EVENT_SKILL_STATE_BONUSES,
)
from domain.utils.sim_time_utils import get_sim_time_from


def _get_active_state_types(contender: BlobCompetitorDto, current_time: int):
    for st in contender.states:
        effect_until_time = get_sim_time_from(
            st.effect_until.season, st.effect_until.epoch, st.effect_until.cycle
        )
        if effect_until_time >= current_time:
            yield st.type


def compute_item_skill_multiplier(
    contender: BlobCompetitorDto, current_time: int
) -> float:
    skill_bonus = sum(
        PRE_EVENT_SKILL_STATE_BONUSES.get(state_type, 0.0)
        for state_type in _get_active_state_types(contender, current_time)
    )
    return 1.0 + skill_bonus


def compute_item_min_score_boost(
    contender: BlobCompetitorDto, current_time: int
) -> float:
    return sum(
        PRE_EVENT_MIN_SCORE_STATE_BONUSES.get(state_type, 0.0)
        for state_type in _get_active_state_types(contender, current_time)
    )


def compute_event_multiplier_from_contender(
    contender: BlobCompetitorDto, current_time: int
) -> tuple[float, bool]:
    """Compute event multiplier from contender's states (avoiding DB fetch).

    Returns (multiplier, focused_active).
    """
    from data.model.state_type import StateType

    multiplier = 1.0
    focused = False
    for st_type in _get_active_state_types(contender, current_time):
        if st_type == StateType.INJURED:
            multiplier *= 0.6
        elif st_type == StateType.TIRED:
            multiplier *= 0.8
        elif st_type == StateType.GLOOMY:
            multiplier *= 0.95
        elif st_type == StateType.FOCUSED:
            focused = True
    return multiplier, focused


def get_random_coefficient(is_focused: bool, min_score_boost: float = 0.0) -> float:
    """Get a random coefficient for score calculation, with a boost if focused."""
    if is_focused:
        min_value = 0.2 + min_score_boost
        return random.random() * (1.0 - min_value) + min_value
    return random.random() * (1.0 - min_score_boost) + min_score_boost


def get_inverse_random_coefficient(
    is_focused: bool, min_score_boost: float = 0.0
) -> float:
    """Get a random coefficient that favors lower values, with a boost if focused."""
    if is_focused:
        return random.random() * 0.8
    return random.random() * max(0.0, 1.0 - min_score_boost)


def generate_race_score_for_contender(
    contender: BlobCompetitorDto, current_time: int, race_duration: int, tick: int
) -> float:
    """
    Generate race score for contender.
    """

    multiplier, focused = compute_event_multiplier_from_contender(
        contender, current_time
    )
    skill_multiplier = compute_item_skill_multiplier(contender, current_time)
    min_score_boost = compute_item_min_score_boost(contender, current_time)

    noise = perlin_like_noise_1d(
        race_duration,
        current_time * contender.id,
        focused,
        min_score_boost,
    )
    return noise[tick] * contender.speed * multiplier * skill_multiplier


@lru_cache(maxsize=128)
def perlin_like_noise_1d(
    length: int, seed: float, is_focused: bool, min_score_boost: float = 0.0
) -> list[float]:
    """
    Generate perlin like noise.
    """
    random.seed(seed)
    result = [get_random_coefficient(is_focused, min_score_boost)]
    for _ in range(length - 1):
        gradient = random.random()
        if gradient < 0.5:
            result.append(
                result[-1]
                * (
                    1
                    - (
                        get_inverse_random_coefficient(is_focused, min_score_boost)
                        * gradient
                        * 2
                    )
                )
            )
        else:
            result.append(
                result[-1] + (1 - result[-1]) * random.random() * (gradient - 0.5) * 2
            )
    random.seed()
    return result
