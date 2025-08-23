import random
from functools import lru_cache

from domain.dtos.blob_competitor_dto import BlobCompetitorDto


def generate_race_score_for_contender(contender: BlobCompetitorDto, current_time: int, race_duration: int, tick: int) -> float:
    """
    Generate race score for contender.
    """
    noise = perlin_like_noise_1d(race_duration, current_time * contender.id)
    return noise[tick] * contender.speed


@lru_cache(maxsize=128)
def perlin_like_noise_1d(length: int, seed: float) -> list[float]:
    """
    Generate perlin like noise.
    """
    random.seed(seed)
    result = [random.random()]
    for _ in range(length - 1):
        gradient = random.random()
        if gradient < 0.5:
            result.append(result[-1] * (1 - (random.random() * gradient * 2)))
        else:
            result.append(result[-1] + (1 - result[-1]) * random.random() * (gradient - 0.5) * 2)
    random.seed()
    return result
