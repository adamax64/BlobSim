import random
from functools import lru_cache

from domain.dtos.blob_competitor_dto import BlobCompetitorDto


def compute_event_multiplier_from_contender(
    contender: BlobCompetitorDto, current_time: int
) -> tuple[float, bool]:
    """Compute event multiplier from contender's states (avoiding DB fetch).

    Returns (multiplier, focused_active).
    """
    from data.model.state_type import StateType

    multiplier = 1.0
    focused = False
    for st in contender.states:
        if st.effect_until < current_time:
            continue
        st_type: StateType = st.type
        if st_type == StateType.INJURED:
            multiplier *= 0.6
        elif st_type == StateType.TIRED:
            multiplier *= 0.8
        elif st_type == StateType.GLOOMY:
            multiplier *= 0.95
        elif st_type == StateType.FOCUSED:
            focused = True
    return multiplier, focused


def get_random_coefficient(is_focused: bool) -> float:
    """Get a random coefficient for score calculation, with a boost if focused."""
    return random.random() * 0.8 + 0.2 if is_focused else random.random()


def get_inverse_random_coefficient(is_focused: bool) -> float:
    """Get a random coefficient that favors lower values, with a boost if focused."""
    return random.random() * 0.8 if is_focused else random.random()


def generate_race_score_for_contender(
    contender: BlobCompetitorDto, current_time: int, race_duration: int, tick: int
) -> float:
    """
    Generate race score for contender.
    """

    multiplier, focused = compute_event_multiplier_from_contender(
        contender, current_time
    )

    noise = perlin_like_noise_1d(race_duration, current_time * contender.id, focused)
    return noise[tick] * contender.speed * multiplier


@lru_cache(maxsize=128)
def perlin_like_noise_1d(length: int, seed: float, is_focused: bool) -> list[float]:
    """
    Generate perlin like noise.
    """
    random.seed(seed)
    result = [get_random_coefficient(is_focused)]
    for _ in range(length - 1):
        gradient = random.random()
        if gradient < 0.5:
            result.append(
                result[-1]
                * (1 - (get_inverse_random_coefficient(is_focused) * gradient * 2))
            )
        else:
            result.append(
                result[-1] + (1 - result[-1]) * random.random() * (gradient - 0.5) * 2
            )
    random.seed()
    return result
