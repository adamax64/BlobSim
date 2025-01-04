from domain.utils.constants import CYCLES_PER_EPOCH, CYCLES_PER_SEASON


def get_season(time: int) -> int:
    return int(time / CYCLES_PER_SEASON) + 1


def is_season_start(time: int) -> bool:
    return time % CYCLES_PER_SEASON == 0


def is_season_end(time: int) -> bool:
    return time % CYCLES_PER_SEASON == CYCLES_PER_SEASON - 1


def get_sim_time_from(season: int, epoch: int, cycle: int) -> int:
    return (season - 1) * CYCLES_PER_SEASON + epoch * CYCLES_PER_EPOCH + cycle
